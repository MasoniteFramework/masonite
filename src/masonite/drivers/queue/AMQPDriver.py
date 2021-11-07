import pickle
import pendulum
import inspect
from ...utils.console import HasColoredOutput


class AMQPDriver(HasColoredOutput):
    def __init__(self, application):
        self.application = application
        self.connection = None
        self.publishing_channel = None

    def set_options(self, options):
        self.options = options
        return self

    def push(self, *jobs, args=(), **kwargs):
        for job in jobs:
            payload = {
                "obj": job,
                "args": args,
                "callback": self.options.get("callback", "handle"),
                "created": pendulum.now(tz=self.options.get("tz", "UTC")),
            }

            try:
                self.connect().publish(payload)
            except (self.get_connection_exceptions()):
                self.connect().publish(payload)

    def get_connection_exceptions(self):
        pika = self.get_package_library()
        return (
            pika.exceptions.ConnectionClosed,
            pika.exceptions.ChannelClosed,
            pika.exceptions.ConnectionWrongStateError,
            pika.exceptions.ChannelWrongStateError,
        )

    def publish(self, payload):
        pika = self.get_package_library()
        self.publishing_channel.basic_publish(
            exchange="",
            routing_key=self.options.get("queue"),
            body=pickle.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,  # make message persistent
            ),
        )
        self.publishing_channel.close()
        self.connection.close()

    def get_package_library(self):
        try:
            import pika
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'pika' library. Run 'pip install pika' to fix this."
            )

        return pika

    def connect(self):
        try:
            import pika
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'pika' library. Run 'pip install pika' to fix this."
            )

        self.connection = pika.BlockingConnection(
            pika.URLParameters(
                "amqp://{}:{}@{}{}/{}".format(
                    self.options.get("username"),
                    self.options.get("password"),
                    self.options.get("host"),
                    ":" + str(self.options.get("port"))
                    if self.options.get("port")
                    else "",
                    self.options.get("vhost", "%2F"),
                )
            )
        )

        self.publishing_channel = self.connection.channel()

        self.publishing_channel.queue_declare(self.options.get("queue"), durable=True)

        return self

    def consume(self):
        self.success(
            '[*] Waiting to process jobs on the "{}" queue. To exit press CTRL+C'.format(
                self.options.get("queue")
            )
        )

        self.connect()

        self.publishing_channel.basic_qos(prefetch_count=1)

        self.publishing_channel.basic_consume(self.options.get("queue"), self.work)

        try:
            self.publishing_channel.start_consuming()
        finally:
            self.publishing_channel.stop_consuming()
            self.publishing_channel.close()
            self.connection.close()

    def retry(self):
        builder = (
            self.application.make("builder")
            .new()
            .on(self.options.get("connection"))
            .table(self.options.get("failed_table", "failed_jobs"))
        )

        jobs = builder.get()

        if len(jobs) == 0:
            self.success("No failed jobs found.")
            return

        for job in jobs:
            try:
                self.connect().publish(pickle.loads(job["payload"]))
            except (self.get_connection_exceptions()):
                self.connect().publish(pickle.loads(job["payload"]))

        self.success(f"Added {len(jobs)} failed jobs back to the queue")
        builder.table(self.options.get("failed_table", "failed_jobs")).where_in(
            "id", [x["id"] for x in jobs]
        ).delete()

    def work(self, ch, method, _, body):

        job = pickle.loads(body)
        obj = job["obj"]
        args = job["args"]
        callback = job["callback"]

        try:
            try:
                if inspect.isclass(obj):
                    obj = self.application.resolve(obj)

                getattr(obj, callback)(*args)

            except AttributeError:
                obj(*args)

            self.success(
                f"[{method.delivery_tag}][{pendulum.now(tz=self.options.get('tz', 'UTC')).to_datetime_string()}] Job Successfully Processed"
            )
        except Exception as e:
            self.danger(
                f"[{method.delivery_tag}][{pendulum.now(tz=self.options.get('tz', 'UTC')).to_datetime_string()}] Job Failed"
            )

            getattr(obj, "failed")(job, str(e))

            self.add_to_failed_queue_table(
                self.application.make("builder").new(), str(job["obj"]), body, str(e)
            )

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def add_to_failed_queue_table(self, builder, name, payload, exception):
        builder.table(self.options.get("failed_table", "failed_jobs")).create(
            {
                "driver": "amqp",
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
