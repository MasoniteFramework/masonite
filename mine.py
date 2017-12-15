import os
import sys
from whitenoise import WhiteNoise
from app.start import app

application = WhiteNoise(app, root='storage/static')
application.add_files('storage/static', prefix='storage/static/')