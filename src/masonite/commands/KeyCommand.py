"""New Key Command."""
from cryptography.fernet import Fernet

from .Command import Command


class KeyCommand(Command):
    """
    Generate a new key.

    key
        {--s|--store : Stores the key in the .env file}
        {--d|--dont-store : Does not store the key in the .env file}
    """

    def handle(self):
        key = bytes(Fernet.generate_key()).decode("utf-8")

        if self.option("dont-store"):
            return self.info(f"Key: {key}")

        with open(".env", "r") as file:
            data = file.readlines()

        for line_number, line in enumerate(data):
            if line.startswith("APP_KEY="):
                data[line_number] = "APP_KEY={}\n".format(key)
                break

        with open(".env", "w") as file:
            file.writelines(data)

        self.info("Key added to your .env file: {}".format(key))
