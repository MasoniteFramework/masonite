''' Database Settings '''
from peewee import *
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

engines = {
    'default': MySQLDatabase(os.environ.get('DB_DATABASE'), user=os.environ.get('DB_USERNAME'), password=os.environ.get('DB_PASSWORD'), host=os.environ.get('DB_HOST'))
}
