import jwt
import pendulum
from masonite.facades import Auth


class Api:
    def __init__(self, application, driver_config=None):
        self.application = application

    def set_configuration(self, config):
        self.config = config
        return self

    def generate_token(self, model):
        secret = self.config.get("jwt").get("secret")
        algorithm = self.config.get("jwt").get("algorithm")
        expire_minutes = self.config.get("jwt").get("expires")
        if expire_minutes:
            expire_minutes = (
                pendulum.now(tz="GMT").add(minutes=expire_minutes).to_datetime_string()
            )
        token = jwt.encode({"expires": expire_minutes}, secret, algorithm=algorithm)

        return token

    def validate_token(self, token):
        secret = self.config.get("jwt").get("secret")
        algorithm = self.config.get("jwt").get("algorithm")
        expire_minutes = self.config.get("jwt").get("expires")
        authenticates = self.config.get("jwt").get("authenticates")
        if expire_minutes:
            expire_minutes = (
                pendulum.now(tz="GMT").add(minutes=expire_minutes).to_datetime_string()
            )

        unencrypted_token = jwt.decode(token, secret, algorithms=[algorithm])
        expires = unencrypted_token.get("expires")
        if not expires:
            return True

        expired = pendulum.parse(expires, tz="GMT").is_past()

        if expired:
            return False

        if authenticates:
            auth = Auth.guard("jwt").attempt_by_token(token)
            return bool(auth)
