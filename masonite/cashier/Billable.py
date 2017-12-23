''' Billable Model which can be added to a user model to charge users '''
from peewee import Model, CharField
import stripe
from config import payment

if payment.DRIVER == 'stripe':
    stripe.api_key = payment.PROCESSORS['stripe']['secret']

class Billable(Model):
    ''' Billable model used for model extensions '''
    stripe_token = CharField(default='')
    stripe_customer_id = CharField(default='')
    payment_processor = CharField(default='')

    def charge(self, amount, token):
        ''' Charge the user with a certain amount '''
        charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,  # obtained with Stripe.js
            description="Charge for " + self.email
        )

        query = self.update(
            stripe_token=token,
            payment_processor=payment.DRIVER,
            stripe_customer_id=charge.id).where(self.id == self.id)
        query.execute()
