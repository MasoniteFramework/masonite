"""__class__ validation"""

from masonite.validation import BaseValidation


class __class__(BaseValidation):
    """__class__ validation class"""

    def passes(self, attribute, key, dictionary):
        """The passing criteria for this rule.

        This should return a True boolean value.

        Arguments:
            attribute {mixed} -- The value found within the dictionary
            key {string} -- The key in the dictionary being searched for.
                            This key may or may not exist in the dictionary.
            dictionary {dict} -- The dictionary being searched

        Returns:
            bool
        """
        return attribute

    def message(self, key):
        """A message to show when this rule fails

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return f"{key} is required"

    def negated_message(self, key):
        """A message to show when this rule is negated using a negation rule like 'isnt()'

        For example if you have a message that says 'this is required' you may have a negated statement
        that says 'this is not required'.

        Arguments:
            key {string} -- The key used to search the dictionary

        Returns:
            string
        """
        return "{key} is not required"
