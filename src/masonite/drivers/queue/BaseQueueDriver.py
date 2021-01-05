"""Base queue driver."""

import pickle

import pendulum

from ...drivers import BaseDriver
from ...helpers import HasColoredCommands


class BaseQueueDriver(BaseDriver, HasColoredCommands):
    def add_to_failed_queue_table(self, payload, channel=None, driver="amqp"):
        from config.database import DB
        from config import queue

        schema = DB.get_schema_builder()

        if schema.has_table("failed_jobs"):
            DB.get_query_builder().table("failed_jobs").create(
                {
                    "driver": driver,
                    "queue": channel,
                    "channel": channel,
                    "payload": pickle.dumps(payload),
                    "failed_at": pendulum.now().to_datetime_string(),
                }
            )

    def run_failed_jobs(self):
        from config.database import DB

        try:
            self.success("Attempting to send failed jobs back to the queue ...")
            builder = DB.get_query_builder()
            jobs = builder.table("failed_jobs").get()
            if not jobs:
                return self.success("No failed jobs found")

            self.success(f"Found {len(jobs)} jobs")
            for job in builder.table("failed_jobs").get():
                payload = pickle.loads(job["payload"])

                builder.table("failed_jobs").where("payload", job["payload"]).delete()
                self.push(
                    payload["obj"], args=payload["args"], callback=payload["callback"]
                )
            self.success("Jobs successfully added back to the queue.")
        except Exception as e:
            raise e
            self.danger("Could not get the failed_jobs table")

    def push(self, *objects, args=(), callback="handle", ran=1, channel=None):
        raise NotImplementedError

    def connect(self):
        return self

    def consume(self, channel, **options):
        raise NotImplementedError(
            "The {} driver does not implement consume".format(self.__class__.__name__)
        )

    def work(self):
        raise NotImplementedError(
            "The {} driver does not implement work".format(self.__class__.__name__)
        )
