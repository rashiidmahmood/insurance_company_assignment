import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'
        django_get_or_create = ('email',)

    first_name = factory.sequence(lambda n: f'first name {n}')
    last_name = factory.sequence(lambda n: f'last name {n}')
    email = factory.sequence(lambda n: f'email{n}@test.com')
