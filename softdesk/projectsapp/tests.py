from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from projectsapp.models import Project


class AppAPITestCase(APITestCase):
    maxDiff = None

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.user = cls.create_user(
            username="user",
            email="user@test.com",
            password="wxcv1234",
            birthdate="1991-03-02",
            can_be_contacted=False,
            can_data_be_shared=False
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
        cls.project1 = Project.objects.create(
            name='project1',
            description='description1',
            author=cls.user,
            type='BACKEND',
        )
        cls.project1.contributors.add(
            cls.user2,
            through_defaults={
                'role': 'CONTRIBUTOR'
            }
        )
        cls.project2 = Project.objects.create(
            name='project2',
            description='description2',
            author=cls.user,
            type='iOS',
        )

    @classmethod
    def create_user(
        cls,
        username,
        email,
        password,
        birthdate,
        can_be_contacted,
        can_data_be_shared
    ):
        User = get_user_model()
        user_data = {
            "username": username,
            "email": email,
            "password": password,
            "birthdate": birthdate,
            "can_be_contacted": can_be_contacted,
            "can_data_be_shared": can_data_be_shared
        }
        user = User.objects.create_user(**user_data)
        user.save()
        return user

    def setUp(self):
        get_token_url = reverse('token-obtain-pair')
        access_token = self.client.post(
            get_token_url,
            {
                "username": "user",
                "password": "wxcv1234"
            }
        ).data.get("access")
        self.client.credentials(
            HTTP_AUTORIZATION=f'Bearer {access_token}'
        )
        self.project1 = Project.objects.get(pk=1)

    def format_datetime(self, value):
        return value.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    def get_project_list_data(self, projects):
        return [
            {
                'id': project.pk,
                'name': project.name,
                'description': project.description,
                'author': project.author.username,
                'type': project.type,
                'time_created': self.format_datetime(project.time_created),
                'contributors': [
                    contributor.username
                    for contributor in project.contributors.all()
                ]
            } for project in projects
        ]

    def get_project_detail_data(self, project):
        return {
            'id': project.pk,
            'name': project.name,
            'description': project.description,
            'author': {
                'id': project.author.id,
                'username': project.author.username,
                'email': project.author.email
            },
            'type': project.type,
            'time_created': self.format_datetime(project.time_created),
            'contributors': [
                {
                    'id': contributor.id,
                    'user': {
                        'id': contributor.user.id,
                        'username': contributor.user.username,
                        'email': contributor.user.email
                    },
                    'role': contributor.role
                }
                for contributor in project.contributor_set.all()
            ],
            'issues': [
                {
                    "name": issue.name,
                    "description": issue.description,
                    "priority": issue.priority,
                    "tag": issue.tag,
                    "status": issue.status,
                    "project": issue.project,
                    "assigned_to": {
                        'id': issue.assigned_to.id,
                        'username': issue.assigned_to.username,
                        'email': issue.assigned_to.email
                    },
                    "author": {
                        'id': issue.author.id,
                        'username': issue.author.username,
                        'email': issue.author.email
                    },
                    "time_created": issue.time_created
                }
                for issue in project.issues.all()
            ]
        }

    def get_response_unauthenticated(self):
        return {
            'detail': 'Authentication credentials were not provided.'
        }


class TestProjectUnauthenticated(AppAPITestCase):
    url_list = reverse_lazy('project-list')
    url_detail = reverse_lazy('project-detail', args=(1,))
    url_add_contributor = reverse_lazy('project-add_contributor', args=(1,))
    url_remove_contributor = reverse_lazy(
        'project-remove_contributor',
        args=(1,)
    )

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )

    def test_create(self):
        project_count = Project.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "name": "project",
                "description": "project description",
                "type": "BACKEND"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Project.objects.count(), project_count)

    def test_add_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_add_contributor,
            data={
                "user": "3"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_remove_contributor,
            data={
                "user": "2"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestProjectAuthenticated(AppAPITestCase):
    url_list = reverse_lazy('project-list')
    url_detail = reverse_lazy('project-detail', args=(1,))
    url_add_contributor = reverse_lazy('project-add_contributor', args=(1,))
    url_remove_contributor = reverse_lazy(
        'project-remove_contributor',
        args=(1,)
    )

    def setUp(self):
        super().setUp()
        self.client.login(username='user', password='wxcv1234')

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_project_list_data(
                [self.project1, self.project2]
            )
        )

    def test_detail(self):
        response = self.client.get(
            self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_project_detail_data(
                self.project1
            )
        )

    def test_create(self):
        project_count = Project.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "name": "project",
                "description": "project description",
                "type": "BACKEND"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Project.objects.count(), project_count + 1)

    def test_add_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_add_contributor,
            data={
                "user": "3"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'status': 'Contributor added'}
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count + 1
        )

    def test_add_existing_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_add_contributor,
            data={
                "user": "1"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'unique constraint failed':
                    [
                        "This contributor already exists"
                    ]
            }
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_add_unexistind_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_add_contributor,
            data={
                "user": "50"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "user": [
                    "Invalid pk \"50\" - object does not exist."
                ]
            }
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_remove_contributor,
            data={
                "user": "2"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {'status': 'Contributor removed'}
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count - 1
        )

    def test_remove_author_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_remove_contributor,
            data={
                "user": "1"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {'detail': 'You cannot remove the author from the contributors'}
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_unexisting_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_remove_contributor,
            data={
                "user": "50"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                "user": [
                    f"Invalid pk 50 - Contributor does not exist."
                ]
            },
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )
