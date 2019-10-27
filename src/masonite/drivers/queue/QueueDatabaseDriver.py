"""Async Driver Method."""

import inspect
import pickle
import time

import pendulum
from masonite.contracts import QueueContract
from masonite.drivers import BaseQueueDriver
from masonite.helpers import HasColoredCommands, parse_human_time
from masonite.queues import Queueable


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
        from config import queue

        callback = options.get('callback', 'handle')
        wait = options.get('wait', None)
        connection = options.get('connection', None)

        if connection:
            schema = schema.connection(connection)

        if wait:
            wait = parse_human_time(wait).to_datetime_string()

        for job in objects:
            if schema.get_schema_builder().has_table('queue_jobs'):
                payload = pickle.dumps({'obj': job, 'args': args, 'callback': callback})
                schema.table('queue_jobs').insert({
                    'name': str(job),
                    'serialized': payload,
                    'created_at': pendulum.now().to_datetime_string(),
                    'attempts': 0,
                    'ran_at': None,
                    'wait_until': wait,
                })

    def consume(self, channel, fair=False, **options):
        from config.database import DB as schema, DATABASES
        from config import queue
        from wsgi import container

        if not channel or channel == 'default':
            channel = DATABASES['default']

        self.info('[*] Waiting to process jobs from the "queue_jobs" table on the "{}" connection. To exit press CTRL + C'.format(channel))
        schema = schema.connection(channel)
        while True:
            jobs = schema.table('queue_jobs').where('ran_at', None).get()
            if not jobs.count():
                time.sleep(5)

            for job in jobs:
                unserialized = pickle.loads(job.serialized)
                obj = unserialized['obj']
                args = unserialized['args']
                callback = unserialized['callback']
                ran = job.attempts

                wait_time = job['wait_until']

                if isinstance(wait_time, str):
                    wait_time = pendulum.parse(job['wait_until'])
                else:
                    wait_time = pendulum.instance(job['wait_until'])

                # print(job['wait_until'], wait_time.is_future())
                if job['wait_until'] and wait_time.is_future():
                    continue
                try:
                    try:
                        if inspect.isclass(obj):
                            obj = container.resolve(obj)

                        getattr(obj, callback)(*args)

                    except AttributeError:
                        obj(*args)

                    try:
                        # attempts = 1
                        schema.table('queue_jobs').where('id', job['id']).update({
                            'ran_at': pendulum.now().to_datetime_string(),
                            'attempts': job['attempts'] + 1,
                        })
                        self.success('[\u2713] Job Successfully Processed')
                    except UnicodeEncodeError:
                        self.success('[Y] Job Successfully Processed')
                except Exception as e:
                    self.danger('Job Failed: {}'.format(str(e)))

                    if not obj.run_again_on_fail:
                        # ch.basic_ack(delivery_tag=method.delivery_tag)
                        schema.table('queue_jobs').where('id', job['id']).update({
                            'ran_at': pendulum.now().to_datetime_string(),
                            'failed': 1,
                            'attempts': job['attempts'] + 1,
                        })

                    if ran < obj.run_times and isinstance(obj, Queueable):
                        time.sleep(1)
                        schema.table('queue_jobs').where('id', job['id']).update({
                            'attempts': job['attempts'] + 1,
                        })
                        continue
                    else:
                        schema.table('queue_jobs').where('id', job['id']).update({
                            'attempts': job['attempts'] + 1,
                            'ran_at': pendulum.now().to_datetime_string(),
                            'failed': 1,
                        })

                        if hasattr(obj, 'failed'):
                            getattr(obj, 'failed')(unserialized, str(e))

                        self.add_to_failed_queue_table(unserialized, driver='database')

            time.sleep(5)
