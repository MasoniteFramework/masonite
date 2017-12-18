''' Payments configuration file '''
import os

'''
|--------------------------------------------------------------------------
| Payment Driver
|--------------------------------------------------------------------------
|
| This is the default payment processor. Setting this driver will make
| all forms of payment processing packages grab the respective info
| from the processors dictionary.
|
| drivers supported: stripe
'''

DRIVER = 'stripe'

PROCESSORS = {
    'stripe' : {
        'key': os.environ.get('STRIPE_PUBLISHABLE'),
        'secret': os.environ.get('STRIPE_SECRET'),
    },
    'braintree': {
        'key': os.environ.get('BRAINTREE_PUBLISHABLE'),
        'secret': os.environ.get('BRAINTREE_SECRET')
    }
}
