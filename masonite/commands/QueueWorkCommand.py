""" A QueueWorkCommand Command """

import inspect
import pickle

from cleo import Command

from config import queue
from masonite.exceptions import DriverLibraryNotFound


def callback(ch, method, properties, body):
    from wsgi import container
    job = pickle.loads(body)
    obj = job['obj']
    args = job['args']
    callback = job['callback']
    if inspect.isclass(obj):
        obj = container.resolve(obj)

    try:
        getattr(obj, callback)(*args)
    except AttributeError:
        obj(*args)

    ch.basic_ack(delivery_tag=method.delivery_tag)


class QueueWorkCommand(Command):
    """
    Start the queue worker

    queue:work
        {--c|channel=default : The channel to listen on the queue}
        {--f|fair : Send jobs to queues that have no jobs instead of randomly selecting a queue}
    """

    def handle(self):
        try:
            import pika
        except ImportError:
            raise DriverLibraryNotFound(
                "Could not find the 'pika' library. Run pip install pika to fix this.")

        connection = pika.BlockingConnection(pika.URLParameters('amqp://{}:{}@{}{}/{}'.format(
            queue.DRIVERS['amqp']['username'],
            queue.DRIVERS['amqp']['password'],
            queue.DRIVERS['amqp']['host'],
            ':' + str(queue.DRIVERS['amqp']['port']) if 'port' in queue.DRIVERS['amqp'] and queue.DRIVERS['amqp']['port'] else '',
            queue.DRIVERS['amqp']['vhost'] if 'vhost' in queue.DRIVERS['amqp'] and queue.DRIVERS['amqp']['vhost'] else '%2F'
        )))
        channel = connection.channel()

        channel.queue_declare(queue=self.option('channel'), durable=True)

        channel.basic_consume(callback,
                              queue=self.option('channel'))
        if self.option('fair'):
            channel.basic_qos(prefetch_count=1)

        self.info(' [*] Waiting to process jobs on the "{}" channel. To exit press CTRL+C'.format(
            self.option('channel')))
        channel.start_consuming()
