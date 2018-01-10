''' Pulls in the gunicorn application '''
from whitenoise import WhiteNoise
from bootstrap.start import app
from config import storage

application = WhiteNoise(app, root='storage/static')

for location, alias in storage.STATICFILES.items():
    application.add_files(location, prefix=alias)
    