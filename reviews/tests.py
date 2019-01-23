import json

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from reviews.models import Review


class UserRegistrationAPIViewTestCase(APITestCase):
    url = '/api/v1/api-auth/register/'

    def test_invalid_password(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': 'password',
            'confirm_password': 'INVALID_PASSWORD'
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_register(self):
        user_data = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': '123123',
            'confirm_password': '123123',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(201, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            'username': 'testuser',
            'email': 'test@testuser.com',
            'password': '123123',
            'confirm_password': '123123',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(201, response.status_code)

        user_data_2 = {
            'username': 'testuser',
            'email': 'test1@testuser.com',
            'password': '123123',
            'confirm_password': '123123',
            'first_name': 'test',
            'last_name': 'test'
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)


class UserObtainTokenAPIViewTestCase(APITestCase):
    url = '/api/v1/api-auth/obtain-api-token/'

    def setUp(self):
        self.username = 'john'
        self.email = 'john@snow.com'
        self.password = 'you_know_nothing'
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_authentication_without_password(self):
        response = self.client.post(self.url, {'username': 'snowman'})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {'username': self.username, 'password': 'I_know'})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in json.loads(response.content))


class UserTokenAPIViewTestCase(APITestCase):
    url = '/api/v1/reviews/'

    def setUp(self):
        self.username = 'user1'
        self.email = 'user1@user.com'
        self.password = 'verysecret'
        self.user_1 = User.objects.create_user(self.username, self.email, self.password)
        self.token_1 = Token.objects.create(user=self.user_1)

        self.user_2 = User.objects.create_user('user2', 'user2@test.com', 'megasecret')
        self.token_2 = Token.objects.create(user=self.user_2)

    def tearDown(self):
        self.user_1.delete()
        self.token_1.delete()
        self.user_2.delete()
        self.token_2.delete()

    def test_post_and_get_reviews(self):
        review_1 = {
            "rating": 0,
            "title": "string",
            "summary": "string",
            "company": "string",
            "reviewer": "string"
        }

        review_2 = {
            "rating": 0,
            "title": "string",
            "summary": "string",
            "company": "string",
            "reviewer": "string"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_1.key)
        response_1 = self.client.post(self.url, data=review_1)
        response_2 = self.client.post(self.url, data=review_2)
        self.assertEqual(201, response_1.status_code)
        self.assertEqual(201, response_2.status_code)

        response_1_get, response_2_get = json.loads(self.client.get(self.url).content)

        self.assertEqual(json.loads(response_1.content), response_1_get)
        self.assertEqual(json.loads(response_2.content), response_2_get)

        # Assert that IP address is there
        for ip in Review.objects.values_list('ip', flat=True):
            self.assertEqual('127.0.0.1', ip)

    def test_post_and_get_reviews_from_different_users(self):
        review_1 = {
            "rating": 0,
            "title": "string",
            "summary": "string",
            "company": "string",
            "reviewer": "string"
        }

        review_2 = {
            "rating": 0,
            "title": "string",
            "summary": "string",
            "company": "string",
            "reviewer": "string"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_1.key)
        response_1 = self.client.post(self.url, data=review_1)
        response_2 = self.client.post(self.url, data=review_2)
        self.assertEqual(201, response_1.status_code)
        self.assertEqual(201, response_2.status_code)

        response_1_get, response_2_get = json.loads(self.client.get(self.url).content)

        self.assertEqual(json.loads(response_1.content), response_1_get)
        self.assertEqual(json.loads(response_2.content), response_2_get)
        # SECOND USER

        review_1_2 = {
            "rating": 2,
            "title": "string2",
            "summary": "string",
            "company": "string",
            "reviewer": "string"
        }

        review_2_2 = {
            "rating": 2,
            "title": "string",
            "summary": "string",
            "company": "string",
            "reviewer": "string2"
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_2.key)
        response_1_2 = self.client.post(self.url, data=review_1_2)
        response_2_2 = self.client.post(self.url, data=review_2_2)
        self.assertEqual(201, response_1_2.status_code)
        self.assertEqual(201, response_2_2.status_code)

        response_1_2_get, response_2_2_get = json.loads(self.client.get(self.url).content)

        self.assertEqual(json.loads(response_1_2.content), response_1_2_get)
        self.assertEqual(json.loads(response_2_2.content), response_2_2_get)
