''' Database Settings '''
import os

from dotenv import find_dotenv, load_dotenv
from peewee import MySQLDatabase

load_dotenv(find_dotenv())

DRIVER = 'mysql'

ENGINES = {
    'default': MySQLDatabase(
        os.environ.get('DB_DATABASE'),
        user=os.environ.get('DB_USERNAME'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'))
}
