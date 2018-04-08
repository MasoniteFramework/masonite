import os

DRIVER = 'ably'

DRIVERS = {
    'pusher': {
        'app_id': os.getenv('PUSHER_APP_ID'),
        'client': os.getenv('PUSHER_CLIENT'),
        'secret': os.getenv('PUSHER_SECRET'),
    },
    'ably': {
        'secret': os.getenv('ABLY_SECRET')
    }
}
