import time
from masonite.queues.Queueable import Queueable


def TryMe():
    time.sleep(5)


class AsyncMe(Queueable):

    def __init__(self, MailSmtpDriver):
        self.mail = MailSmtpDriver

    def handle(self):
        self.mail.to('idmann509@gmail.com').send('from asyncme')
        return 'hey'
