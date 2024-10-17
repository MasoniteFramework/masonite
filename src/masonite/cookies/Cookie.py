from ..configuration import config


class Cookie:
    def __init__(self, name, value, **options):
        self.options = options

        self.name = name
        self.value = value
        self.http_only = self.__get_option('http_only', True)
        self.secure = self.__get_option('secure', False)
        self.expires = self.__get_option('expires', None)
        self.timezone = self.__get_option('timezone', None)
        self.samesite = self.__get_option('samesite', 'Strict')
        self.path = self.__get_option('path', '/')
        self.encrypt = self.__get_option('encrypt', True)

    def render(self):
        response = f"{self.name}={self.value};"
        if self.http_only:
            response += "HttpOnly;"
        if self.secure:
            response += "Secure;"
        if self.expires:
            if self.timezone:
                response += f"Expires={self.expires} {self.timezone};"
            else:
                response += f"Expires={self.expires};"
        if self.path:
            response += f"Path={self.path};"
        if self.samesite:
            response += f"SameSite={self.samesite};"

        return response

    def __get_option(self, key: str, default: any):
        """
            Get cookie options from config/session.py
            if option key found in options then it return that
            if not found in options then it will fetch from config
            if not found in config then use the default value
        """
        if key in self.options:
            return self.options[key]
        else:
            cookie = config('session.drivers.cookie')
            return cookie[key] if key in cookie else default
