from masonite.drivers.BaseMailDriver import BaseMailDriver
import smtplib

from email.message import EmailMessage

class MailSmtpDriver(BaseMailDriver):

    def send(self, message_contents):
        config = self.config.DRIVERS['smtp']

        message = EmailMessage()
        message.set_content(message_contents)
        message['Subject'] = self.message_subject
        message['From'] = '{0} <{1}>'.format(self.config.FROM['name'], self.config.FROM['address'])
        message['To'] = self.to_address

        # Send the message via our own SMTP server.
        s = smtplib.SMTP('{0}:{1}'.format(config['host'], config['port']))
        s.login(config['username'], config['password'])
        s.send_message(message)
        s.quit()
