"""Async Driver Method."""

import inspect
import pickle
import time

import pendulum
from ...contracts import QueueContract
from ...drivers import BaseQueueDriver
from ...helpers import HasColoredCommands, parse_human_time
from ...queues import Queueable
from .QueueJobsModel import QueueJobsModel


class QueueDatabaseDriver(BaseQueueDriver, HasColoredCommands, QueueContract):
    """Queue Aysnc Driver."""

    def __init__(self):
        """Queue Async Driver.

        Arguments:
            Container {masonite.app.App} -- The application container.
        """
        pass

    def connect(self):
        return self

    def push(self, *objects, args=(), kwargs={}, **options):
        """Push objects onto the async stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
            options {**kwargs of options} - Additional options for async driver
        """

        from config.database import DB as schema
        from masoniteorm.query import QueryBuilder

        callback = options.get("callback", "handle")
        wait = options.get("wait", None)
        connection = options.get("connection", "default")
        queue = options.get("queue", "default")

        if wait:
            wait = parse_human_time(wait).to_datetime_string()

        for job in objects:
            if schema.get_schema_builder(connection).has_table("queue_jobs"):
                payload = pickle.dumps(
                    {"obj": job, "args": args, "kwargs": kwargs, "callback": callback}
                )

                schema.get_query_builder(connection).table("queue_jobs").create(
                    {
                        "name": str(job),
                        "serialized": payload,
                        "created_at": pendulum.now().to_datetime_string(),
                        "attempts": 0,
                        "ran_at": None,
                        "queue": queue,
                        "available_at": wait,
                        "reserved_at": None,
                    }
                )

    def consume(self, channel, **options):  # skipcq
        from config.database import DB, DATABASES
        from wsgi import container

        self.info(
            '[*] Waiting to process jobs from the "queue_jobs" table on the "{}" connection. To exit press CTRL + C'.format(
                channel
            )
        )

        builder = QueueJobsModel
        while True:
            jobs = (
                builder.where_null("ran_at")
                .where_null("reserved_at")
                .where("queue", options.get("queue", "default"))
                .where(
                    lambda q: q.where_null("available_at").or_where(
                        "available_at", "<=", pendulum.now().to_datetime_string()
                    )
                )
                .limit(5)
                .order_by("id")
                .get()
            )

            builder.where_in("id", jobs.pluck("id")).update(
                {"reserved_at": pendulum.now().to_datetime_string()}
            )

            if not jobs.count():
                time.sleep(int(options.get("poll")) or 1)
                continue

            for job in jobs:
                builder.where("id", job["id"]).update(
                    {
                        "ran_at": pendulum.now().to_datetime_string(),
                    }
                )
                unserialized = pickle.loads(job["serialized"])
                obj = unserialized["obj"]
                args = unserialized["args"]
                callback = unserialized["callback"]

                try:
                    try:
                        if inspect.isclass(obj):
                            obj = container.resolve(obj)

                        getattr(obj, callback)(*args)

                    except AttributeError:
                        obj(*args)

                    try:
                        self.success("[\u2713] Job Successfully Processed")
                    except UnicodeEncodeError:
                        self.success("[Y] Job Successfully Processed")
                    builder.where("id", job["id"]).delete()
                except Exception as e:  # skipcq
                    self.danger("Job Failed: {}".format(str(e)))

                    # if not obj.run_again_on_fail:
                    builder.where("id", job["id"]).delete()

                    if hasattr(obj, "failed"):
                        getattr(obj, "failed")(unserialized, str(e))
                    self.add_to_failed_queue_table(
                        unserialized, channel=channel, driver="database"
                    )
