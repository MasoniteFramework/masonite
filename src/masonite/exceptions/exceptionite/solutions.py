class TableNotFound:
    def title(self):
        return "Table Not Found"

    def description(self):
        return "You are trying to make a query on a table that cannot be found. Check that :table migration exists and that migrations have been ran with 'python craft migrate' command."

    def regex(self):
        return r"no such table: (?P<table>(\w+))"


class MissingCSRFToken:
    def title(self):
        return "Missing CSRF Token"

    def description(self):
        return "You are trying to make a sensitive request without providing a CSRF token. Your request might be vulnerable to Cross Site Request Forgery. To resolve this issue you should use {{ csrf_field }} in HTML forms or add X-CSRF-TOKEN header in AJAX requests."

    def regex(self):
        return r"Missing CSRF Token"


class InvalidCSRFToken:
    def title(self):
        return "The session does not match the CSRF token"

    def description(self):
        return "Try clearing your cookies for the localhost domain in your browsers developer tools."

    def regex(self):
        return r"Invalid CSRF Token"


class TemplateNotFound:
    def title(self):
        return "Template Not Found"

    def description(self):
        return """':template.html' view file has not been found in registered view locations. Please verify the spelling of the template and that it exists in locations declared in Kernel file. You can check
        available view locations with app.make('view.locations')."""

    def regex(self):
        return r"Template '(?P<template>(\w+))' not found"


class NoneResponse:
    def title(self):
        return "Response cannot be None"

    def description(self):
        return """Ensure that the controller method used in this request returned something. A controller method cannot return None or nothing.
        If you don't want to return a value you can return an empty string ''."""

    def regex(self):
        return r"Responses cannot be of type: None."


class RouteMiddlewareNotFound:
    def title(self):
        return "Did you register the middleware key in your Kernel.py file?"

    def description(self):
        return "Check your Kernel.py file inside your 'route_middleware' attribute and look for a :middleware key"

    def regex(self):
        return r"Could not find the \'(?P<middleware>(\w+))\' middleware key"
