"""Validation Module."""

import validator


class Validator:
    """Validator Class. Responsible for validating form data and dictionaries."""

    def __init__(self, request=None):
        """Validator constructor.

        Keyword Arguments:
            request {masonite.request.Request} -- Request class. (default: {None})
        """
        self.request = request
        self.validation_dictionary = {}
        self.check_manual_dictionary = False
        self.error_messages = {}

    def validate(self, dictionary):
        """Set the validation dictionary.

        Arguments:
            dictionary {dict} -- Dictionary to validate

        Returns:
            self
        """
        self.validation_dictionary = dictionary
        return self

    def check(self, check_manual_dictionary=False):
        """Validate the dictionary.

        Keyword Arguments:
            check_manual_dictionary {bool} -- Check a dictionary manually. (default: {False})

        Returns:
            bool|dict
        """
        if check_manual_dictionary:
            self.check_manual_dictionary = check_manual_dictionary
        return self.run_validation()[0]

    def errors(self):
        """Return a dictionary of errors.

        Returns:
            None|dict
        """
        validation = self.run_validation()
        for message in self.error_messages:
            if message in validation[1]:
                validation[1][message] = self.error_messages[message]

        if not validation[1]:
            return None

        return validation[1]

    def run_validation(self):
        """Load the dictionary and runs the validations.

        Returns:
            bool|dict
        """
        validation_dict = self.load_request_input()
        for validation in validation_dict:
            validation_dict.update({
                validation: self.get(validation)
            })

        return validator.validate(self.validation_dictionary, validation_dict)

    def get(self, validation):
        """Get a key in the validation input and runs it through a cast method if one exists.

        Arguments:
            validation {string} -- Key inside the validation input

        Returns:
            string -- Returns the validation
        """
        if hasattr(self, "cast_{}".format(validation)):
            validation_input = self.load_request_input()[validation]
            return getattr(self, "cast_{}".format(validation))(validation_input)

        return self.load_request_input()[validation]

    def error(self, error_id):
        """Get an error from the error dictionary by key.

        Arguments:
            error_id {string} -- Error key to search for.

        Returns:
            string|None
        """
        if error_id in self.errors():
            return self.errors()[error_id]

        return None

    def load_request_input(self):
        """Find which input to load into the validation.

        Returns:
            dict -- Returns the dictionary of values to validate.
        """
        if self.request:
            return self.request.all().copy()

        return self.check_manual_dictionary

    def messages(self, messages):
        """Specify custom error messages if the validation fails.

        Arguments:
            messages {dict} -- Sets a dictionary of error messages.
        """
        self.error_messages = messages
