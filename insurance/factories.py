import factory
import random

from customer.factories import CustomerFactory

from insurance.models import Policy


class PolicyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'insurance.Policy'

    type = random.choice(list(Policy.TYPES._db_values))
    premium = factory.sequence(lambda n: n)
    cover = factory.sequence(lambda n: n)


class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'insurance.Quote'

    policy = factory.SubFactory(PolicyFactory)
    customer = factory.SubFactory(CustomerFactory)
