# Create your tests here.
from json import dumps
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework import status
from rest_framework.test import RequestsClient, APITestCase

from event_manager.models import MyUser


class RestTest(APITestCase):
    def setUp(self):
        self.login = "test_name"
        self.email = 'ff@ff.ff'
        self.pwd = "test_pwd"
        self.user = MyUser.objects.create_user(
            username=self.login,
            password=self.pwd,
            email=self.email
        )

    def test_create_token(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Token.objects.get(user=self.user).__str__(),
            response.json()['token']
        )

    def test_bad_create_token(self):
        url = reverse("create-token")
        data = {
            "login": 'badtest',
            "email": 'badtest',
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_event(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        client = RequestsClient()
        headers = {'Authorization': 'Token ' + Token.objects.get(user=self.user).key}
        response = client.get('http://127.0.0.1:8000/event/addevent', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_event(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        client = RequestsClient()

        headers = {'Authorization': 'Token ' + Token.objects.get(user=self.user).key}
        data = {
            "event": 'testevent',
            "date_event": '2021-02-23',
            "time_start": '10:00',
        }
        response = client.post('http://127.0.0.1:8000/event/addevent', headers=headers, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_your_events(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        client = RequestsClient()
        headers = {'Authorization': 'Token ' + Token.objects.get(user=self.user).key}
        response = client.get('http://127.0.0.1:8000/event/yourevents', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_yourmonthevents(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        client = RequestsClient()
        headers = {'Authorization': 'Token ' + Token.objects.get(user=self.user).key}
        response = client.get('http://127.0.0.1:8000/event/yourmonthevents', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_holidays(self):
        url = reverse("create-token")
        data = {
            "login": self.login,
            "email": self.email,
            "pwd": self.pwd
        }
        response = self.client.post(
            path=url,
            data=dumps(data),
            content_type="application/json"
        )
        client = RequestsClient()
        headers = {'Authorization': 'Token ' + Token.objects.get(user=self.user).key}
        response = client.get('http://127.0.0.1:8000/event/holidays', headers=headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
