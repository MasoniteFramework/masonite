from masoniteorm.models import Model


class QueueJobsModel(Model):
    __table__ = "queue_jobs"
    __timestamps__ = None
