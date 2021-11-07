import pickle
import pendulum
from ...utils.console import HasColoredOutput
from ...utils.time import parse_human_time
import time


class DatabaseDriver(HasColoredOutput):
    def __init__(self, application):
        self.application = application

    def set_options(self, options):
        self.options = options
        return self

    def push(self, *jobs, args=(), **kwargs):
        builder = self.get_builder()

        available_at = parse_human_time(kwargs.get("delay", "now"))

        for job in jobs:
            payload = pickle.dumps(
                {
                    "obj": job,
                    "args": args,
                    "kwargs": kwargs,
                    "callback": self.options.get("callback", "handle"),
                }
            )

            builder.create(
                {
                    "name": str(job),
                    "payload": payload,
                    "available_at": available_at.to_datetime_string(),
                    "attempts": 0,
                    "queue": self.options.get("queue", "default"),
                }
            )

    def consume(self):
        print("Listening for jobs on queue: " + self.options.get("queue", "default"))
        builder = self.get_builder()

        while True:
            time.sleep(int(self.options.get("poll", 1)))
            if self.options.get("verbosity") == "vv":
                print("Checking for available jobs .. ")
            builder = builder.new().table(self.options.get("table"))
            jobs = (
                builder.where("queue", self.options.get("queue", "default"))
                .where(
                    "available_at",
                    "<=",
                    pendulum.now(tz=self.options.get("tz", "UTC")).to_datetime_string(),
                )
                .limit(10)
                .order_by("id")
                .get()
            )

            if self.options.get("verbosity") == "vv":
                print(f"Found {len(jobs)} job(s) ")

            builder.where_in("id", [x["id"] for x in jobs]).update(
                {
                    "reserved_at": pendulum.now(
                        tz=self.options.get("tz", "UTC")
                    ).to_datetime_string()
                }
            )

            for job in jobs:
                builder.where("id", job["id"]).table(self.options.get("table")).update(
                    {
                        "ran_at": pendulum.now(
                            tz=self.options.get("tz", "UTC")
                        ).to_datetime_string(),
                    }
                )
                payload = job["payload"]
                unserialized = pickle.loads(job["payload"])
                obj = unserialized["obj"]
                args = unserialized["args"]
                callback = unserialized["callback"]

                try:
                    try:
                        getattr(obj, callback)(*args)

                    except AttributeError:
                        obj(*args)

                    self.success(
                        f"[{job['id']}][{pendulum.now(tz=self.options.get('tz', 'UTC')).to_datetime_string()}] Job Successfully Processed"
                    )
                    if self.options.get("verbosity") == "vv":
                        print(f"Successful. Deleting Job ID: {job['id']}")
                    builder.where("id", job["id"]).delete()
                except Exception as e:  # skipcq
                    self.danger(
                        f"[{job['id']}][{pendulum.now(tz=self.options.get('tz', 'UTC')).to_datetime_string()}] Job Failed"
                    )

                    if job["attempts"] + 1 < self.options.get("attempts", 1):
                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).update(
                            {
                                "attempts": job["attempts"] + 1,
                            }
                        )
                    elif job["attempts"] + 1 >= self.options.get(
                        "attempts", 1
                    ) and not self.options.get("failed_table"):
                        # Delete the jobs
                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).update(
                            {
                                "attempts": job["attempts"] + 1,
                            }
                        )

                        if hasattr(obj, "failed"):
                            getattr(obj, "failed")(unserialized, str(e))

                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).delete()
                    elif self.options.get("failed_table"):
                        self.add_to_failed_queue_table(
                            builder, job["name"], payload, str(e)
                        )

                        if hasattr(obj, "failed"):
                            getattr(obj, "failed")(unserialized, str(e))

                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).delete()
                    else:
                        builder.where("id", job["id"]).table(
                            self.options.get("table")
                        ).update(
                            {
                                "attempts": job["attempts"] + 1,
                            }
                        )

    def retry(self):
        builder = self.get_builder()

        jobs = (
            builder.table(self.options.get("failed_table"))
            .where("queue", self.options.get("queue", "default"))
            .get()
        )

        if len(jobs) == 0:
            self.success("No failed jobs found.")
            return

        for job in jobs:
            builder.table("jobs").create(
                {
                    "name": str(job["name"]),
                    "payload": job["payload"],
                    "attempts": 0,
                    "available_at": pendulum.now(
                        tz=self.options.get("tz", "UTC")
                    ).to_datetime_string(),
                    "queue": job["queue"],
                }
            )
        self.success(f"Added {len(jobs)} failed job(s) back to the queue")
        builder.table(self.options.get("failed_table", "failed_jobs")).where_in(
            "id", [x["id"] for x in jobs]
        ).delete()

    def get_builder(self):
        return (
            self.application.make("builder")
            .new()
            .on(self.options.get("connection"))
            .table(self.options.get("table"))
        )

    def add_to_failed_queue_table(self, builder, name, payload, exception):
        builder.table(self.options.get("failed_table", "failed_jobs")).create(
            {
                "driver": "database",
                "queue": self.options.get("queue", "default"),
                "name": name,
                "connection": self.options.get("connection"),
                "created_at": pendulum.now(
                    tz=self.options.get("tz", "UTC")
                ).to_datetime_string(),
                "exception": exception,
                "payload": payload,
                "failed_at": pendulum.now(
                    tz=self.options.get("tz", "UTC")
                ).to_datetime_string(),
            }
        )
