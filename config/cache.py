''' Cache Settings '''

import os

'''
|--------------------------------------------------------------------------
| Cache Driver
|--------------------------------------------------------------------------
|
| Caching is a great way to gain an instant speed boost to your application.
| Very often templates will not change and you can utilize caching to the
| best by caching your templates forever, monthly or every few seconds
|
| Supported: 'disk'
|
'''

DRIVER = os.getenv('CACHE_DRIVER', 'disk')

'''
|--------------------------------------------------------------------------
| Cache Drivers
|--------------------------------------------------------------------------
|
| Place all your caching coniguration as a dictionary here. The keys here
| should correspond to the driver types supported above.
|
'''

DRIVERS = {
    'disk': {
        'location': 'bootstrap/cache'
    }
}
