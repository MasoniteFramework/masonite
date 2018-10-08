"""
Cache configuration
"""

import os

DRIVER = 'disk'

DRIVERS = {
    'disk': {
        'location': 'bootstrap/cache'
    },
    'redis': {
        'host': os.getenv('REDIS_HOST', 'localhost'),
        'port': os.getenv('REDIS_PORT', '6379'),
        'password': os.getenv('REDIS_PASSWORD', '')
    }
}
