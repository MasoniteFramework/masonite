import os
import sys
from whitenoise import WhiteNoise
from app.start import app

application = WhiteNoise(app, root='storage/static')