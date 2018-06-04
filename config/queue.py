''' Queue Settings '''

import os

'''
|--------------------------------------------------------------------------
| Queue Driver
|--------------------------------------------------------------------------
|
| Queues are an excellent way to send intensive and time consuming tasks
| into the background to improve performance of your application.
|
| Supported: 'async'
|
'''

DRIVER = os.getenv('QUEUE_DRIVER', 'async')

'''
|--------------------------------------------------------------------------
| Queue Drivers
|--------------------------------------------------------------------------
|
| Put any configuration settings for your drivers in this configuration
| setting.
|
'''

DRIVERS = {}
