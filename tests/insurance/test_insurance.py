from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from insurance.models import Quote
from users.factories import UserFactory
from customer.factories import CustomerFactory
from insurance.factories import PolicyFactory, QuoteFactory
from customer.models import Customer


class Tests(APITestCase):
    def setUp(self) -> None:
        super().setUp()

    def force_login(self, user):
        self.client.force_login(user=user)

    def test_should_not_allow_quote_creation_without_authentication(self):
        policy = PolicyFactory()
        customer = CustomerFactory()

        data = {
            'policy': policy.id,
            'customer': customer.id
        }
        response = self.client.post(
            reverse('insurance_api:quote-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertContains(
            response,
            'Authentication credentials were not provided.',
            status_code=status.HTTP_403_FORBIDDEN
        )

    def test_should_not_allow_customer_to_create_quote_for_other_customers(self):
        policy = PolicyFactory()
        customer1 = CustomerFactory()
        customer2 = CustomerFactory()

        self.force_login(customer1.user)

        data = {
            'policy': policy.id,
            'customer': customer2.id
        }
        response = self.client.post(
            reverse('insurance_api:quote-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(
            response,
            'Invalid customer!',
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_quote_creation(self):
        policy = PolicyFactory()
        customer = CustomerFactory()

        self.force_login(customer.user)

        data = {
            'policy': policy.id,
            'customer': customer.id
        }
        response = self.client.post(
            reverse('insurance_api:quote-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Quote.objects.count(), 1
        )

    def test_allow_staff_to_accept_the_quote(self):
        user = UserFactory(is_staff=True)
        policy = PolicyFactory()
        customer = CustomerFactory()
        quote = QuoteFactory(policy=policy, customer=customer)

        self.force_login(user)

        data = {
            'state': 'accepted'
        }
        response = self.client.put(
            reverse('insurance_api:quote-detail', kwargs={'pk': quote.id}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Quote.objects.count(), 1
        )
        self.assertEqual(
            Quote.objects.first().state, 'accepted'
        )

    def test_allow_staff_to_make_the_quote_active(self):
        user = UserFactory(is_staff=True)
        policy = PolicyFactory()
        customer = CustomerFactory()
        quote = QuoteFactory(policy=policy, customer=customer)

        self.force_login(user)

        data = {
            'state': 'active'
        }
        response = self.client.put(
            reverse('insurance_api:quote-detail', kwargs={'pk': quote.id}),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Quote.objects.count(), 1
        )
        self.assertEqual(
            Quote.objects.first().state, 'active'
        )

    def test_list_policies(self):
        user = UserFactory(is_staff=True)
        self.force_login(user)

        self.assertFalse(Quote.objects.all().exists())

        quote1 = QuoteFactory()
        quote2 = QuoteFactory()
        quote3 = QuoteFactory()

        response = self.client.get(
            reverse('insurance_api:policy-list'),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)
        self.assertContains(response, quote1.customer.dob)
        self.assertContains(response, quote2.policy.premium)
        self.assertContains(response, quote3.customer.user.email)

    def test_filter_by_customer_name_in_list_policies(self):
        user = UserFactory(is_staff=True)
        self.force_login(user)

        self.assertFalse(Quote.objects.all().exists())

        customer1 = CustomerFactory(user=UserFactory(first_name='Rashid', last_name='Mahmood'))
        customer2 = CustomerFactory(user=UserFactory(first_name='Ali', last_name='Hassan'))
        QuoteFactory(customer=customer1)
        QuoteFactory(customer=customer2)
        QuoteFactory(customer=customer1)

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_name={customer1.user.first_name}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertContains(response, f'{customer1.user.last_name}')

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_name={customer2.user.last_name}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertNotContains(response, f'{customer1.user.first_name}')

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_name={customer1.user.last_name}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_name=Qasim",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_filter_by_customer_dob_in_list_policies(self):
        user = UserFactory(is_staff=True)
        self.force_login(user)

        self.assertFalse(Quote.objects.all().exists())

        customer1 = CustomerFactory(dob='1991-11-04')
        customer2 = CustomerFactory(dob='1980-01-02')
        customer3 = CustomerFactory(dob='2000-12-10')
        QuoteFactory(customer=customer1)
        QuoteFactory(customer=customer2)
        QuoteFactory(customer=customer1)
        QuoteFactory(customer=customer3)

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_dob={customer1.dob}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertContains(response, f'{customer1.user.last_name}')

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_dob={customer2.dob}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertNotContains(response, f'{customer1.user.first_name}')
        self.assertNotContains(response, f'{customer3.user.last_name}')

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_dob={customer3.dob}",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        response = self.client.get(
            f"{reverse('insurance_api:policy-list')}?customer_dob=2001-01-01",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

