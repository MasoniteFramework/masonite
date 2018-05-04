import requests
from masonite.contracts.MailContract import MailContract
from masonite.drivers.BaseMailDriver import BaseMailDriver
from masonite.drivers.BaseDriver import BaseDriver


class MailMailgunDriver(BaseMailDriver, MailContract):
    """
    Mailgun driver
    """
    def send(self, message=None):
        if not message:
            message = self.message_body

        domain = self.config.DRIVERS['mailgun']['domain']
        secret = self.config.DRIVERS['mailgun']['secret']
        return requests.post(
            "https://api.mailgun.net/v3/{0}/messages".format(domain),
            auth=("api", secret),
            data={
                "from": "{0} <mailgun@{1}>".format(self.config.FROM['name'], domain),
                "to": [self.to_address, "{0}".format(self.config.FROM['address'])],
                "subject": self.message_subject,
                "html": message})
