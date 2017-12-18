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

'''
|--------------------------------------------------------------------------
| Payment Processors
|--------------------------------------------------------------------------
|
| This will list the processors thay your project will require. New
| processors can be added simply and third party libraries can
| use this information.
|
'''

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
