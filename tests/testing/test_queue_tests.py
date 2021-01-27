from tests.queues.test_drivers import Job, FailJob
from src.masonite.testing import TestCase
from src.masonite.drivers.queue.BaseQueueDriver import BaseQueueDriver as Queue
from src.masonite.queues.Queueable import Queueable


class JobWithArgs(Queueable):

    def handle(self, arg1=None):
        print('sending from job handled', arg1)
        return 'test'


class TestMockQueues(TestCase):

    def setUp(self):
        super().setUp()
        self.queue = Queue.fake()

    def tearDown(self):
        super().tearDown()
        self.queue = Queue.restore()

    def test_mock_push(self):
        self.queue.assertNothingPushed()
        self.queue.driver("database").push(Job)
        self.queue.driver("database").push(Job)
        self.queue.driver("database").push(Job, channel="test")
        self.queue.assertPushed(Job, count=3)

    def test_mock_push_on_channel(self):
        self.queue.assertNothingPushed()
        self.queue.driver("database").push(Job, channel="high")
        self.queue.assertPushedOn(Job, "high")

    def test_mock_with_failing_jobs(self):
        self.queue.driver("database").push(FailJob)
        self.queue.assertNothingPushed()
        self.queue.driver("database").push(FailJob, channel="low")
        self.queue.assertNothingPushed()

    def test_assert_push_two_jobs_in_same_line(self):
        self.queue.assertNothingPushed()
        self.queue.driver("database").push(Job, JobWithArgs)
        self.queue.assertPushed(Job)
        self.queue.assertPushed(JobWithArgs)

    def test_assert_push_job_with_args(self):
        self.queue.assertNothingPushed()
        self.queue.driver("database").push(JobWithArgs, args=(4,))
        self.queue.assertPushed(JobWithArgs)
