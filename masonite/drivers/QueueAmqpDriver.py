""" Driver for AMQP support """

import pickle
import threading

from config import queue
from masonite.contracts import QueueContract
from masonite.drivers import BaseDriver
from masonite.exceptions import DriverLibraryNotFound

if 'amqp' in queue.DRIVERS:
    listening_channel = queue.DRIVERS['amqp']['channel']
else:
    listening_channel = 'default'


class QueueAmqpDriver(QueueContract, BaseDriver):

    def __init__(self, Container):
        """Queue AMQP Driver

        Arguments:
            Container {masonite.app.App} -- The application container.
        """

        # Start the connection
        self._connect()

    def _connect(self):
        try:
            import pika
            self.pika = pika
        except ImportError:
            raise DriverLibraryNotFound(
                "Could not find the 'pika' library. Run pip install pika to fix this.")

        connection = pika.BlockingConnection(pika.URLParameters('amqp://{}:{}@{}{}/{}'.format(
            queue.DRIVERS['amqp']['username'],
            queue.DRIVERS['amqp']['password'],
            queue.DRIVERS['amqp']['host'],
            ':' +
            queue.DRIVERS['amqp']['port'] if 'port' in queue.DRIVERS['amqp'] and queue.DRIVERS['amqp']['port'] else '',
            queue.DRIVERS['amqp']['vhost'] if 'vhost' in queue.DRIVERS['amqp'] and queue.DRIVERS['amqp']['vhost'] else '%2F'
        )))

        # Get the channel
        self.channel = connection.channel()

        # Declare what queue we are working with
        self.channel.queue_declare(queue=listening_channel, durable=True)

    def _publish(self, body):
        self.channel.basic_publish(exchange='',
                                   routing_key=listening_channel,
                                   body=pickle.dumps(
                                       body
                                   ),
                                   properties=self.pika.BasicProperties(
                                       delivery_mode=2,  # make message persistent
                                   ))

    def push(self, *objects, args=()):
        """Push objects onto the amqp stack.

        Arguments:
            objects {*args of objects} - This can be several objects as parameters into this method.
        """

        for obj in objects:
            # Publish to the channel for each object
            try:
                self._publish({'obj': obj, 'args': args})
            except self.pika.exceptions.ConnectionClosed:
                self._connect()
                self._publish({'obj': obj, 'args': args})
