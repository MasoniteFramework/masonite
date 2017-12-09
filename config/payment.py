import os

driver = 'stripe'

processors = {
    'stripe' : {
        'key': os.environ.get('STRIPE_PUBLISHABLE'),
        'secret': os.environ.get('STRIPE_SECRET'),
    },
    'braintree': {
        'key': os.environ.get('BRAINTREE_PUBLISHABLE'),
        'secret': os.environ.get('BRAINTREE_SECRET')
    }
}
