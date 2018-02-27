''' Broadcast Settings '''

import os

'''
|--------------------------------------------------------------------------
| Broadcast Driver
|--------------------------------------------------------------------------
|
| Realtime support is critical for any modern web application. Broadcast
| drivers allow you to push data from your server to all your clients
| to show data updates to your clients in real time without having
| to constantly refresh the page or send constant ajax requests
|
| Supported: 'pusher', 'ably'
|
'''

DRIVER = os.getenv('BROADCAST_DRIVER', 'pusher')

'''
|--------------------------------------------------------------------------
| Broadcast Drivers
|--------------------------------------------------------------------------
|
| Below is a dictionary of all your driver configurations. Each key in the
| dictionary should be the name of a driver.
|
'''

DRIVERS = {
    'pusher': {
        'app_id': os.getenv('PUSHER_APP_ID', '29382xx..'),
        'client': os.getenv('PUSHER_CLIENT', 'shS8dxx..'),
        'secret': os.getenv('PUSHER_SECRET', 'HDGdjss..'),
    },
    'ably': {
        'secret': os.getenv('ABLY_SECRET', 'api:key')
    }
}
