"""
Storage configuration
"""
from dotenv import find_dotenv, load_dotenv
import os


"""
|--------------------------------------------------------------------------
| Load Environment Variables
|--------------------------------------------------------------------------
|
| Take environment variables from the .env file and load them in.
|
"""

load_dotenv(find_dotenv())

DRIVER = 'disk'

DRIVERS = {
    'disk': {
        'location': {
            'uploading': 'uploads/'
        }
    },
    's3': {
        'client': os.environ.get('S3_CLIENT'),
        'secret': os.environ.get('S3_SECRET'),
        'bucket': os.environ.get('S3_BUCKET'),
        'location': 'http://s3.amazon.com/bucket'
    }
}

SASSFILES = {
    'importFrom': [
        'storage/static'
    ],
    'includePaths': [
        'storage/static/sass'
    ],
    'compileTo': 'storage/compiled'
}

STATICFILES = {
    'storage/static': 'static/',
}
