""" Masonite Validator Module """

from validator import *


class Validator:
    """ 
    Validator Class 
    """

    def __init__(self, request=None):
        self.request = request
        self.validation_dictionary = {}
        self.check_manual_dictionary = False
        self.error_messages = {}

    def validate(self, dictionary):
        """ Sets the validation dictionary """
        self.validation_dictionary = dictionary
        return self

    def check(self, check_manual_dictionary=False):
        """ Validated the dictionary """
        if check_manual_dictionary:
            self.check_manual_dictionary = check_manual_dictionary
        return self.run_validation()[0]

    def errors(self):
        """ Returns Errors """
        validation = self.run_validation()
        for message in self.error_messages:
            if message in validation[1]:
                validation[1][message] = self.error_messages[message]

        if not validation[1]:
            return None

        return validation[1]

    def run_validation(self):
        """ Loads the dictionary and runs the validations """
        validation_dict = self.load_request_input()
        for validation in validation_dict:
            validation_dict.update({
                validation: self.get(validation)
            })

        return validate(self.validation_dictionary, validation_dict)
    
    def get(self, validation):
        if hasattr(self, "cast_{}".format(validation)):
            validation_input = self.load_request_input()[validation]
            return getattr(self, "cast_{}".format(validation))(validation_input)
        
        return self.load_request_input()[validation]
    
    def error(self, error_id):
        if error_id in self.errors():
            return self.errors()[error_id]
        
        return None

    def load_request_input(self):
        if self.request:
            return self.request.all().copy()

        return self.check_manual_dictionary

    def messages(self, messages):
        """ You may change the default messages here """
        self.error_messages = messages
