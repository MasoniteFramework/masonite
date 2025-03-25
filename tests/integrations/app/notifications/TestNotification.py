from src.masonite.notification import Notification
from src.masonite.mail import Mailable
from src.masonite.notification import Sms

class TestNotification(Notification, Mailable):

    def to_vonage(self, notifiable):
        return Sms().text("Test message" )

    def via(self, notifiable):
        return ["vonage"]