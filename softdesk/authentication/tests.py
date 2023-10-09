from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient


User = get_user_model()


class UserTestCase(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.get_token_url = reverse('token-obtain-pair')
        cls.user = cls.create_user(
            username="user",
            email="user@test.com",
            password="wxcv1234",
            birthdate="1991-03-02",
            can_be_contacted=False,
            can_data_be_shared=False,
            superuser=True
        )
        cls.user2 = cls.create_user(
            username="user2",
            email="user2@test.com",
            password="wxcv1234",
            birthdate="1994-05-11",
            can_be_contacted=False,
            can_data_be_shared=False
        )
        cls.create_user(
            username="user3",
            email="user3@test.com",
            password="wxcv1234",
            birthdate="1999-03-23",
            can_be_contacted=False,
            can_data_be_shared=False
        )

    @classmethod
    def create_user(
        cls,
        username,
        email,
        password,
        birthdate,
        can_be_contacted,
        can_data_be_shared,
        superuser=False
    ):
        User = get_user_model()
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "birthdate": datetime.strptime(birthdate, "%Y-%m-%d"),
            "can_be_contacted": can_be_contacted,
            "can_data_be_shared": can_data_be_shared
        }
        if superuser:
            user = User.objects.create_superuser(**user_data)
        else:
            user = User.objects.create_user(**user_data)
        user.save()
        return user

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%d")

    def get_user_list_data(self, users):
        return [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "birthdate": self.format_datetime(user.birthdate),
                "can_be_contacted": user.can_be_contacted,
                "can_data_be_shared": user.can_data_be_shared
            } for user in users
        ]

    def get_user_detail_data(self, user):
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "birthdate": self.format_datetime(user.birthdate),
            "can_be_contacted": user.can_be_contacted,
            "can_data_be_shared": user.can_data_be_shared
        }

    def get_response_unauthenticated(self):
        return {
            'detail': 'Authentication credentials were not provided.'
        }

    def get_response_not_permited(self):
        return {
            "detail": "You do not have permission to perform this action."
        }


class UserAsAdmin(UserTestCase):
    url_list = reverse_lazy('user-list')
    url_detail = reverse_lazy('user-detail', args=(2,))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.access_token = cls.client.post(
            cls.get_token_url,
            {
                "username": "user",
                "password": "wxcv1234"
            }
        ).data.get("access")

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_is_superuser(self):
        user = User.objects.get(pk=1)
        self.assertTrue(user.is_superuser)

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_user_list_data(
                User.objects.all()
            )
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_user_detail_data(self.user2)
        )

    def test_create(self):
        user_count = User.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "username": "test",
                "email": "test@exemple.com",
                "password": "wxcv1234",
                "birthdate": "1980-05-20",
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username='test'))
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_create_less_than_15_years_old(self):
        user_count = User.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "username": "test",
                "email": "test@exemple.com",
                "password": "wxcv1234",
                "birthdate": "2010-01-01",
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "birthdate": [
                    "You must have over 15 years old to create an account"
                ]
            }
        )
        self.assertEqual(User.objects.count(), user_count)

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "username": "new_username",
                "password": "new_password"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.user2.refresh_from_db()
        self.assertEqual(
            self.user2.username,
            "new_username"
        )
        self.assertTrue(self.user2.check_password('new_password'))

    def test_delete(self):
        user_count = User.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(User.objects.count(), user_count - 1)


class UserAsNormalUser(UserTestCase):
    url_list = reverse_lazy('user-list')
    url_detail_owner = reverse_lazy('user-detail', args=(2,))
    url_detail_other = reverse_lazy('user-detail', args=(1,))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.access_token = cls.client.post(
            cls.get_token_url,
            {
                "username": "user2",
                "password": "wxcv1234"
            }
        ).data.get("access")

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_is_superuser(self):
        user = User.objects.get(pk=2)
        self.assertFalse(user.is_superuser)

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )

    def test_detail_owner(self):
        response = self.client.get(self.url_detail_owner)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_user_detail_data(self.user2)
        )

    def test_detail_other(self):
        response = self.client.get(self.url_detail_other)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )

    def test_create(self):
        user_count = User.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "username": "test",
                "email": "test@exemple.com",
                "password": "wxcv1234",
                "birthdate": "1980-05-20",
                "can_be_contacted": True,
                "can_data_be_shared": True
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.get(username='test'))
        self.assertEqual(User.objects.count(), user_count + 1)

    def test_update_owner(self):
        response = self.client.patch(
            self.url_detail_owner,
            data={
                "username": "new_username"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.user2.refresh_from_db()
        self.assertEqual(
            self.user2.username,
            "new_username"
        )

    def test_update_other(self):
        response = self.client.patch(
            self.url_detail_other,
            data={
                "username": "new_username"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.user.refresh_from_db()
        self.assertEqual(
            self.user.username,
            "user"
        )

    def test_delete(self):
        user_count = User.objects.count()
        response = self.client.delete(self.url_detail_other)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(User.objects.count(), user_count)


class UserAsUnauthenticatedUser(UserTestCase):
    url_list = reverse_lazy('user-list')
    url_detail = reverse_lazy('user-detail', args=(2,))

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )
