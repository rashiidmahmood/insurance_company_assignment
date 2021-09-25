import datetime

import factory
from factory.fuzzy import FuzzyDate

from users.factories import UserFactory


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'customer.Customer'

    user = factory.SubFactory(UserFactory)
    dob = FuzzyDate(
        start_date=(datetime.date(1980, 1, 1)),
        end_date=(datetime.date(2000, 12, 30))
    )
