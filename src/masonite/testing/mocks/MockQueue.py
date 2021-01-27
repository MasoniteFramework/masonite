import collections
from functools import reduce
import inspect

from ...drivers.queue.BaseQueueDriver import BaseQueueDriver

def makehash():
    return collections.defaultdict(makehash)

def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


class MockQueue(BaseQueueDriver):

    def __init__(self, container=None, immediate=False):
        self.container = container
        self._run = immediate

        self.queued_jobs = makehash()
        self.failed_jobs = makehash()

    def push(self, *objects, args=(), kwargs={}, **options):

        callback = options.get("callback", "handle")

        for job in objects:
            # transform job to be queued in an instance
            if inspect.isclass(job):
                job, job_name = self.container.resolve(job), job.__name__
            else:
                job_name = job.__class__.__name__

            queue = options.get("channel", None) or options.get("queue", None) or "all"
            data = {
                "job": job,
                "queue": queue,
                "args": args,
                "options": options
            }
            path = f"{queue}.{str(job_name)}"
            try:
                # run task immediately if required
                if self._run:
                    getattr(job, callback)(*args, **kwargs)
            except:
                print("Job failed !")
                self._store_fail(data, path)
            else:
                self._store_success(data, path)

    def _store_fail(self, data, path):
        jobs = deep_get(self.failed_jobs, path)
        if jobs:
            jobs.append(data)
        else:
            self.failed_jobs[path.split(".")[0]][path.split(".")[1]] = [data]

    def _store_success(self, data, path):
        jobs = deep_get(self.queued_jobs, path)
        if jobs:
            jobs.append(data)
        else:
            self.queued_jobs[path.split(".")[0]][path.split(".")[1]] = [data]

    def driver(self, driver):
        return self

    def assertNothingPushed(self):
        return not self.queued_jobs

    def assertPushed(self, job, test_method=None, count=1):
        matching_jobs = []
        for jobs_in_queue in self.queued_jobs.values():
            matching_jobs += jobs_in_queue.get(str(job.__name__), [])
        assert len(matching_jobs) == count
        # check if first job pushed pass the test
        if test_method and count > 0:
            job = matching_jobs[0]["job"]
            job_args = matching_jobs[0]["args"]
            job_channel = matching_jobs[0]["channel"]
            test_method(job, job_args, job_channel)

    def assertPushedAndFail(self, job, test_method=None, count=1):
        matching_jobs = []
        for jobs_in_queue in self.failed_jobs.values():
            matching_jobs += jobs_in_queue.get(str(job.__name__), [])
        assert len(matching_jobs) == count
        # check if first job pushed pass the test
        if test_method and count > 0:
            job = matching_jobs[0]["job"]
            job_args = matching_jobs[0]["args"]
            job_channel = matching_jobs[0]["channel"]
            test_method(job, job_args, job_channel)

    def assertNotPushed(self, job, count=1):
        matching_jobs = []
        for jobs_in_queue in self.queued_jobs.values():
            matching_jobs += jobs_in_queue.get(str(job.__name__), [])
        assert len(matching_jobs) != count

    def assertPushedWithArgs(self, job, args, count=1):
        matching_jobs = []
        for jobs_in_queue in self.queued_jobs.values():
            matching_jobs += jobs_in_queue.get(str(job.__name__), [])
        assert len(matching_jobs) == count
        # check if args are corresponding
        for j in matching_jobs:
            job_args = j["args"]
            assert job_args == args

    def assertPushedOn(self, job, queue, count=1):
        """Assert that a job has been pushed onto a given {queue}, {count} times."""
        assert len(self.queued_jobs[queue][str(job.__name__)]) == count
