## Introduction

Masonite Clerk provides a very expressive and simple syntax to start charging your users with Stripe. In addition to being incredibly easy to setup, Clerk can handle charges, subscriptions, cancellation, subscription swapping, subscription prorating and customer creation. You're going to love it.

### Configuration

#### Pip
First we'll need to install Clerk on our machine. To do this simply run:

    $ pip install clerk

#### Adding The Configuration File

Masonite uses the `config/payment.py` configuration file. Conveniently, Clerk comes with a `publish` command we can use to create this.

#### NOTE: Virtual Environment

**If you are in a virtual environment, `craft publish` will not have access to your virtual environment dependencies. In order to fix this, we can add our site packages to our `config/packages.py` config file**

If you are in a virtual environment then go to your `config/packages.py` file and add your virtual environments site_packages folder to the `SITE_PACKAGES` list. Your `SITE_PACKAGES` list may look something like:

```python
SITE_PACKAGES = [
    'venv/lib/python3.6/site-packages'
]
```

This will allow `craft publish` to find our dependencies installed on our virtual environment.

#### Craft Publish

If you are in a virtual environment it is important you add your virtual environments site_packages directory to the `config/packages.py` file.

We can now run:

    $ craft publish clerk

This will create a new configuration file in `config/payment.py`

#### API Keys

You'll notice in this new `config/payment.py` file we have a config setting that looks like:

```python
PROCESSORS = {
    'stripe': {
        'key': os.environ.get('STRIPE_PUBLISHABLE'),
        'secret': os.environ.get('STRIPE_SECRET'),
        'currency': 'usd'
    }
}
```

Our API keys for `key`, and `secret` should reside in our `.env` file. Just create two entries in your .env file that looks like:

```
STRIPE_PUBLISHABLE=pk_test_Hghus...
STRIPE_SECRET=sk_test_KIsnsh...
```

These API keys can be found in your Stripe dashboard.

#### Database Migrations

We'll assume you want to add billable services to your users so we'll just add a few fields to our users table. Just run something like:

    $ craft migration add_stripe_to_users --table users

Inside this migrations `up()` folder we'll just copy these columns in:

```python
with self.schema.table('users') as table:
    table.string('stripe_id').nullable()
    table.string('card_brand').nullable()
    table.string('card_last_four').nullable()
    table.timestamp('trial_ends_at').nullable()
```

Next we'll do the same thing but will be creating a subscriptions table.

    $ craft migration create_subscriptions_table --create subscriptions

Now just copy and paste these migrations in:

```python
with self.schema.create('subscriptions') as table:
    table.increments('id')
    table.integer('user_id')
    table.string('name')
    table.string('stripe_id')
    table.string('stripe_plan')
    table.integer('quantity')
    table.timestamp('trial_ends_at').nullable()
    table.timestamp('ends_at').nullable()
    table.timestamps()
```

Now that we've finished out migrations let merge it into our database:

    $ craft migrate

#### Billable Model

Lastly we'll add a special class to our users table so we can gain access to a lot of Clerk methods on our model. Let's open our User model and add a new Billable model as well as inherit from it:

```python
from orator import DatabaseManager, Model
from config.database import Model

# New Billable Import
from clerk.Billable import Billable

class User(Model, Billable):

    __fillable__ = ['name', 'email', 'password']

    __auth__ = 'email'

```

That's it! You're all ready to start charging and subscribing users!

## Subscriptions and Charges

**NOTE: All references to token are stripe tokens which are sent by the request after a form submission. For testing purposes you can use the 'tok_amex' string which will create a test AMEX card we don't have to keep submitting forms**

To charge a user $1. All amounts are in cents. So below we are charging our user 1000 cents (or $10)

    User.find(1).charge(token, 1000)

To create a customer

    User.find(1).customer(token)

To subcribe a user to a plan

    User.find(1).subscribe('database_plan', 'stripe_plan', token)

To get the actual subscription model from our payment processor. This is great if you want to make some changes to the subscription manually and the `.save()` it after.

    User.find(1).getSubscription()

To cancel the current subscription

    User.find(1).cancel()

To get the Customer object from our payment processor. This is great if you want to make changes to the customer object manually and then `.save()` it

    User.find(1).getCustomer()

To delete the user as a customer:

    User.find(1).deleteCustomer()

To swap the current processor plan for a new plan. This will prorate the current plan by default.

    User.find(1).swap('new_stripe_plan')

If you do not wish to prorate the user. Read more about prorating from the payment processor you are using.

    User.find(1).noProrate().swap('new_stripe_plan')

Check if a user is subscribed to a specific stripe plan

    User.find(1).subscribedToPlan('stripe_plan')

Check to see if a user is subscribed to any one of the plans specified

    User.find(1).subscribedToPlan(['stripe-plan1', 'stripe-plan2'])

To see if the user is currently subscribed (to any plan)

    User.find(1).subscribed()

To see if a user is subscribed to a specific plan (a local plan, not a stripe plan)

    User.find(1).subscribed('main-plan')

To see if a user is subscribed to any of the plans specified (local plans, not a stripe plans)

    User.find(1).subscribed(['main-plan', 'second-plan'])

