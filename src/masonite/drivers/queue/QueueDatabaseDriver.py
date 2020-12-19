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
        connection = options.get("connection", None)
        queue = options.get("queue", "default")

        if connection:
            schema = schema.connection(connection)

        if wait:
            wait = parse_human_time(wait).to_datetime_string()

        for job in objects:
            if schema.get_schema_builder().has_table("queue_jobs"):
                payload = pickle.dumps(
                    {"obj": job, "args": args, "kwargs": kwargs, "callback": callback}
                )

                schema.get_query_builder().table("queue_jobs").create(
                    {
                        "name": str(job),
                        "serialized": payload,
                        "created_at": pendulum.now().to_datetime_string(),
                        "attempts": 0,
                        "ran_at": None,
                        "queue": queue,
                        "available_at": wait,
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

        schema = DB.get_schema_builder(connection=channel)
        builder = QueueJobsModel
        while True:
            jobs = (
                builder.where_null("ran_at")
                .where_null("reserved_at")
                .where(lambda q: q.where_null("available_at").or_where("available_at", "<=", pendulum.now().to_datetime_string()))
                .limit(5)
                .order_by('id')
                .get()
            )

            builder.where_in('id', jobs.pluck('id')).update({'reserved_at': pendulum.now().to_datetime_string()})

            if not jobs.count():
                time.sleep(int(options.get("poll")) or 1)
                continue

            for job in jobs:
                builder.where("id", job["id"]).update(
                    {
                        "ran_at": pendulum.now().to_datetime_string(),
                    }
                )
                unserialized = pickle.loads(job['serialized'])
                obj = unserialized["obj"]
                args = unserialized["args"]
                callback = unserialized["callback"]
                ran = job['attempts']

                try:
                    try:
                        if inspect.isclass(obj):
                            obj = container.resolve(obj)

                        getattr(obj, callback)(*args)

                    except AttributeError:
                        obj(*args)

                    try:
                        # attempts = 1
                        builder.where("id", job["id"]).update(
                            {
                                "ran_at": pendulum.now().to_datetime_string(),
                                "attempts": job["attempts"] + 1,
                            }
                        )
                        self.success("[\u2713] Job Successfully Processed")
                    except UnicodeEncodeError:
                        self.success("[Y] Job Successfully Processed")
                except Exception as e:  # skipcq
                    self.danger("Job Failed: {}".format(str(e)))

                    if not obj.run_again_on_fail:
                        # ch.basic_ack(delivery_tag=method.delivery_tag)
                        builder.where("id", job["id"]).update(
                            {
                                "ran_at": pendulum.now().to_datetime_string(),
                                "failed": 1,
                                "attempts": job["attempts"] + 1,
                            }
                        )

                    if ran < obj.run_times and isinstance(obj, Queueable):
                        time.sleep(1)
                        builder.where("id", job["id"]).update(
                            {"attempts": job["attempts"] + 1}
                        )
                        continue
                    else:
                        builder.where("id", job["id"]).update(
                            {
                                "attempts": job["attempts"] + 1,
                                "ran_at": pendulum.now().to_datetime_string(),
                                "failed": 1,
                            }
                        )

                        if hasattr(obj, "failed"):
                            getattr(obj, "failed")(unserialized, str(e))

                        self.add_to_failed_queue_table(unserialized, channel=channel, driver="database")
