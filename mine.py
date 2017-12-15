import os
import sys
from whitenoise import WhiteNoise
from app.start import app
from config import storage

application = WhiteNoise(app, root='storage/static')

for location, alias in storage.STATICFILES.iteritems():
    application.add_files(location, prefix=alias)
