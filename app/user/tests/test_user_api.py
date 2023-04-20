""" Unit testing for User API Endpoints """

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """ Create and return a test user """
    return get_user_model().objects.create(**params)


class PublicUserAPITests(TestCase):
    """ Tests for unauthenticated requests """

    def SetUp(self):
        self.client = APIClient()
    
    def test_user_create_successful(self):
        """ Test creating a user is successful """

        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])

        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ Test 400 response for attempt to sign up with existing email """

        create_user(
            email='test@example.com',
            password='testpass123'
        )

        payload = {
            email: 'test@example.com',
            password: 'testpass123',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Test 400 response for attempt to sign up with short password """

        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'test',
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.get(email=payload['email']).exists()
        self.assertFalse(user_exists)
