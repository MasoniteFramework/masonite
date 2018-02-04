import os

'''
|--------------------------------------------------------------------------
| From Address
|--------------------------------------------------------------------------
|
| This value will be used for the default address when sending emails from
| your application.
|
'''

FROM = {
    'address': os.getenv('MAIL_FROM_ADDRESS', 'hello@example.com'),
    'name': os.getenv('MAIL_FROM_NAME', 'Masonite')
}

'''
|--------------------------------------------------------------------------
| Mail Driver
|--------------------------------------------------------------------------
|
| The default driver you will like to use for sending emails. You may add
| additional drivers as you need or pip install additional drivers.
|
| Supported: 'smtp', 'mailgun'
|
'''

DRIVER = os.getenv('MAIL_DRIVER', 'smtp')

'''
|--------------------------------------------------------------------------
| Application Name
|--------------------------------------------------------------------------
|
| This value is the name of your application. This value is used when the
| framework needs to place the application's name in a notification or
| any other location as required by the application or its packages.
|
'''

DRIVERS = {
    'smtp': {
        'host': os.getenv('MAIL_HOST', 'smtp.mailtrap.io'),
        'port': os.getenv('MAIL_PORT', '465'),
        'username': os.getenv('MAIL_USERNAME', 'username'),
        'password': os.getenv('MAIL_PASSWORD', 'password'),
    },
    'mailgun': {
        'secret': os.getenv('MAILGUN_SECRET', 'key-XX'),
        'domain': os.getenv('MAILGUN_DOMAIN', 'sandboxXX.mailgun.org')
    }
}
