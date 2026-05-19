"""Vonage notification driver."""
import re

from ....exceptions import NotificationException
from ..BaseDriver import BaseDriver


class VonageDriver(BaseDriver):
    def __init__(self, application):
        self.app = application
        self.options = {}

    def set_options(self, options):
        self.options = options
        return self

    def build(self, notifiable, notification):
        """Build SMS payload sent to Vonage API."""
        sms = self.get_data("vonage", notifiable, notification)
        if not sms._from:
            sms = sms.from_(self.options.get("sms_from"))
        if not sms._to:
            recipients = notifiable.route_notification_for("vonage")
            sms = sms.to(recipients)
        return sms

    def get_sms_client(self):
        """Return the vonage.Vonage SMS sub-client (SDK v4+)."""
        try:
            from vonage import Vonage, Auth
        except ImportError:
            raise ModuleNotFoundError(
                "Could not find the 'vonage' library. Run 'pip install vonage' to fix this."
            )
        client = Vonage(
            auth=Auth(
                api_key=self.options.get("key"),
                api_secret=self.options.get("secret"),
            )
        )
        return client.sms

    def send(self, notifiable, notification):
        """Send the SMS via Vonage SDK v4."""
        from vonage_sms import SmsMessage
        from vonage_sms.errors import SmsError, PartialFailureError

        sms = self.build(notifiable, notification)
        sms_client = self.get_sms_client()

        recipients = sms._to
        if not isinstance(recipients, list):
            recipients = [recipients]

        response = None
        for recipient in recipients:
            if not self.is_valid_phone_number(recipient):
                raise NotificationException(f"Invalid phone number: {recipient}")

            payload = sms.to(recipient).build().get_options()
            message = SmsMessage(
                to=payload.get("to"),
                from_=payload.get("from"),
                text=payload.get("text"),
            )
            try:
                response = sms_client.send(message)
            except SmsError as exc:
                # vonage 4.x raises SmsError with "error code N: <text>"
                # Reformat into the same NotificationException shape as before
                # so callers and tests can match on "Code [N]".
                match = re.search(r"error code (\d+):\s*(.*)", str(exc))
                if match:
                    code, text = match.group(1), match.group(2).strip()
                    raise NotificationException(
                        "Vonage Code [{0}]: {1}. "
                        "Please refer to API documentation for more details.".format(
                            code, text
                        )
                    )
                raise NotificationException(str(exc))
            except PartialFailureError as exc:
                raise NotificationException(str(exc))

        return response

    def _handle_errors(self, response):
        """Kept for backward compatibility; error handling is now in send()."""
        pass

    def is_valid_phone_number(self, phone_number):
        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(phone_number, None)
            return phonenumbers.is_valid_number(parsed_number)
        except phonenumbers.NumberParseException:
            return False
