from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.factories import UserFactory
from customer.factories import CustomerFactory
from customer.models import Customer


class Tests(APITestCase):
    def setUp(self) -> None:
        super().setUp()

    def test_create_should_not_work_without_email(self):
        data = {
            'first_name': 'Rashid',
            'last_name': 'Mahmood',
            'dob': '1991-11-04'
        }
        response = self.client.post(
            reverse('customer_api:customer-list'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'email', status_code=status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'This field is required.', status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_should_enforce_unique_email(self):
        CustomerFactory(user=UserFactory(email='rashiidmahmood@gmail.com'))

        self.assertEqual(Customer.objects.count(), 1)

        data = {
            'email': 'rashiidmahmood@gmail.com',
            'first_name': 'Rashid',
            'last_name': 'Mahmood',
            'dob': '1991-11-04'
        }
        response = self.client.post(
            reverse('customer_api:customer-list'),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertContains(response, 'Email already exists!', status_code=status.HTTP_400_BAD_REQUEST)

    def test_create_new_customer(self):
        self.assertEqual(
            Customer.objects.count(), 0
        )

        data = {
            'email': 'rashiidmahmood@gmail.com',
            'first_name': 'Rashid',
            'last_name': 'Mahmood',
            'dob': '1991-11-04'
        }
        response = self.client.post(
            reverse('customer_api:customer-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Customer.objects.count(), 1
        )
        self.assertContains(response, 'Rashid', status_code=status.HTTP_201_CREATED)

