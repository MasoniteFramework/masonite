""" Session Settings """

import os

"""
|--------------------------------------------------------------------------
| Session Driver
|--------------------------------------------------------------------------
|
| Sessions are able to be linked to an individual user and carry data from
| request to request. The memory driver will store all the session data
| inside memory which will delete when the server stops running.
|
| Supported: 'memory', 'cookie'
|
"""

DRIVER = os.getenv('SESSION_DRIVER', 'cookie')
