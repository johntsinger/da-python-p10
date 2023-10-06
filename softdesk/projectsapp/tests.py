from django.urls import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.test import APITestCase, APIClient
from projectsapp.models import (
    Project,
    Issue,
    Comment,
)


class AppAPITestCase(APITestCase):
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
            cls.user,
            through_defaults={
                'role': 'AUTHOR'
            }
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
        cls.project2.contributors.add(
            cls.user,
            through_defaults={
                'role': 'AUTHOR'
            }
        )

        cls.issue1 = Issue.objects.create(
            author=cls.user,
            project=cls.project1,
            assigned_to=cls.project1.contributor_set.get(pk=1),
            name="issue1",
            description="issue1 description",
            priority="LOW",
            tag="BUG",
            status="To Do",
        )

        cls.comment1 = Comment.objects.create(
            description="comment1 description",
            issue=cls.issue1,
            author=cls.user
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
            } for project in projects
        ]

    def get_project_detail_data(self, project):
        return {
            'id': project.pk,
            'name': project.name,
            'description': project.description,
            'author': project.author.username,
            'type': project.type,
            'time_created': self.format_datetime(project.time_created),
            'contributors': [
                {
                    'id': contributor.id,
                    'user': contributor.user.username,
                    'role': contributor.role
                }
                for contributor in project.contributor_set.all()
            ],
            'open_issues_count': project.issues.filter(
                ~Q(status='Finished')
            ).count(),
            'closed_issues_count': project.issues.filter(
                Q(status='Finished')
            ).count()
        }

    def get_contributor_list_data(self, contributors):
        return [
            {
                "id": contributor.id,
                "user": contributor.user.username,
                "role": contributor.role,
            } for contributor in contributors
        ]

    def get_contributor_detail_data(self, contributor):
        return {
            "id": contributor.id,
            "user": {
                "id": contributor.user.id,
                "username": contributor.user.username,
                "email": contributor.user.email
            },
            "role": contributor.role,
            "project": contributor.project.name
        }

    def get_issue_list_data(self, issues):
        return [
            {
                "id": issue.id,
                "author": issue.author.username,
                "project": issue.project.name,
                "assigned_to": issue.assigned_to.user.username,
                "name": issue.name,
                "description": issue.description,
                "priority": issue.priority,
                "tag": issue.tag,
                "status": issue.status,
            } for issue in issues
        ]

    def get_issue_detail_data(self, issue):
        return {
            "id": issue.id,
            "author": issue.author.username,
            "project": issue.project.name,
            "assigned_to": issue.assigned_to.user.username,
            "comments_count": issue.comments.count(),
            "name": issue.name,
            "description": issue.description,
            "priority": issue.priority,
            "tag": issue.tag,
            "status": issue.status,
            "time_created": self.format_datetime(issue.time_created)
        }

    def get_comment_list_data(self, comments):
        return [
            {
                "id": str(comment.id),
                "author": comment.author.username,
                "issue": comment.issue.name,
                "description": comment.description,
                "time_created": self.format_datetime(comment.time_created)
            } for comment in comments
        ]

    def get_comment_detail_data(self, comment):
        return {
            "id": str(comment.id),
            "author": comment.author.username,
            "issue": comment.issue.name,
            "description": comment.description,
            "time_created": self.format_datetime(comment.time_created)
        }

    def get_response_unauthenticated(self):
        return {
            'detail': 'Authentication credentials were not provided.'
        }

    def get_response_not_contributor(self, project):
        message = "You must be a contributor to access this project."
        if project.author.can_be_contacted:
            message += (
                " Contact the project owner to "
                f"ask for an access : {project.author.email}"
            )
        return {
            "detail": f"{message}"
        }

    def get_response_not_permited(self):
        return {
            "detail": "You do not have permission to perform this action."
        }

    def get_response_not_found(self):
        return {
            "detail": "Not found."
        }


class TestProjectAsAuthor(AppAPITestCase):
    """Test Project for an authenticated author"""
    url_list = reverse_lazy('project-list')
    url_detail = reverse_lazy('project-detail', args=(1,))

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
        project = Project.objects.get(name='project')
        # test if author is in contributors
        self.assertIn(
            project.author,
            Project.objects.get(name='project').contributors.all()
        )
        self.assertEqual(project.contributor_set.first().role, 'AUTHOR')

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "name": "project renamed"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.project1.refresh_from_db()
        self.assertEqual(
            self.project1.name,
            "project renamed"
        )

    def test_delete(self):
        project_count = Project.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Project.objects.count(), project_count - 1)


class TestProjectAsContributor(AppAPITestCase):
    """Test Project for an authenticated contributor"""
    url_detail = reverse_lazy('project-detail', args=(1,))

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

    def test_delete(self):
        project_count = Project.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(Project.objects.count(), project_count)

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "name": "project renamed"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.project1.refresh_from_db()
        self.assertEqual(
            self.project1.name,
            "project1"
        )


class TestProjectAsNotAuthenticated(AppAPITestCase):
    """Test Project for an unauthenticated user"""
    url_list = reverse_lazy('project-list')
    url_detail = reverse_lazy('project-detail', args=(1,))

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
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )
        self.assertEqual(Project.objects.count(), project_count)

    def test_delete(self):
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.json(),
            self.get_response_unauthenticated()
        )


class TestContributorAsAuthor(AppAPITestCase):
    url_list = reverse_lazy('project-contributor-list', args=(1,))
    url_detail_author = reverse_lazy(
        'project-contributor-detail',
        args=(1, 1)
    )
    url_detail_contributor = reverse_lazy(
        'project-contributor-detail',
        args=(1, 2)
    )

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

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_contributor_list_data(self.project1.contributor_set.all())
        )

    def test_detail(self):
        response = self.client.get(self.url_detail_author)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_contributor_detail_data(
                self.project1.contributor_set.first()
            )
        )

    def test_add_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_list,
            data={
                "user": "user3"
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json(),
            {
                "id": 4,
                "user": "user3",
                "role": "CONTRIBUTOR",
                "project": "project1"
            }
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count + 1
        )

    def test_add_existing_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_list,
            data={
                "user": "user2"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'unique constraint failed':
                    [
                        "This contributor already exists."
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
            self.url_list,
            data={
                "user": "user5"
            }
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {
                'user': ['User object with username=user5 does not exist.']
            }
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail_contributor,
        )
        self.assertEqual(response.status_code, 204)
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count - 1
        )

    def test_remove_author_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail_author,
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json(),
            {'detail': 'You cannot remove the author from the contributors.'
                ' Delete the project instead.'}
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestContributorAsContributor(AppAPITestCase):
    url_list = reverse_lazy('project-contributor-list', args=(1,))
    url_detail_author = reverse_lazy(
        'project-contributor-detail',
        args=(1, 1)
    )
    url_detail_contributor = reverse_lazy(
        'project-contributor-detail',
        args=(1, 2)
    )

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

    def test_add_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_list,
            data={
                "user": "user3"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail_contributor,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestContributorAsNotContributor(AppAPITestCase):
    url_list = reverse_lazy('project-contributor-list', args=(1,))
    url_detail_author = reverse_lazy(
        'project-contributor-detail',
        args=(1, 1)
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.access_token = cls.client.post(
            cls.get_token_url,
            {
                "username": "user3",
                "password": "wxcv1234"
            }
        ).data.get("access")

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )

    def test_detail(self):
        response = self.client.get(self.url_detail_author)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )

    def test_add_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.post(
            self.url_list,
            data={
                "user": "user3"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )

    def test_remove_contributor(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail_author,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestIssueAsAuthor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-list', args=(1,))
    url_detail = reverse_lazy('project-issue-detail', args=(1, 1))

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

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_issue_list_data(
                [self.issue1]
            )
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_issue_detail_data(self.issue1)
        )

    def test_create(self):
        issue_count = Issue.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "assigned_to": 'user2',
                "name": "issue2",
                "description": "issue2 description",
                "priority": "LOW",
                "tag": "BUG",
                "status": "Finished",
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Issue.objects.count(), issue_count + 1)

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "name": "issue1 renamed"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.issue1.refresh_from_db()
        self.assertEqual(
            self.issue1.name,
            "issue1 renamed"
        )

    def test_delete(self):
        issue_count = Issue.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Issue.objects.count(), issue_count - 1)


class TestIssueAsNotAuthor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-list', args=(1,))
    url_detail = reverse_lazy('project-issue-detail', args=(1, 1))

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

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "name": "issue1 updated"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )

    def test_delete(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestIssueAsNotContributor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-list', args=(1,))
    url_detail = reverse_lazy('project-issue-detail', args=(1, 1))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.access_token = cls.client.post(
            cls.get_token_url,
            {
                "username": "user3",
                "password": "wxcv1234"
            }
        ).data.get("access")

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )


class TestCommentAsAuthor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-comment-list', args=(1, 1))

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
        cls.url_detail = reverse_lazy(
            'project-issue-comment-detail',
            args=(1, 1, cls.comment1.id)
        )

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()['results'],
            self.get_comment_list_data(
                [self.comment1]
            )
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            self.get_comment_detail_data(self.comment1)
        )

    def test_create(self):
        comment_count = Comment.objects.count()
        response = self.client.post(
            self.url_list,
            data={
                "description": "comment1 description",
            }
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Comment.objects.count(), comment_count + 1)

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "description": "comment1 description changed"
            }
        )
        self.assertEqual(response.status_code, 200)
        self.comment1.refresh_from_db()
        self.assertEqual(
            self.comment1.description,
            "comment1 description changed"
        )

    def test_delete(self):
        comment_count = Comment.objects.count()
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Comment.objects.count(), comment_count - 1)


class TestCommentAsNotAuthor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-comment-list', args=(1, 1))

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
        cls.url_detail = reverse_lazy(
            'project-issue-comment-detail',
            args=(1, 1, cls.comment1.id)
        )

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_update(self):
        response = self.client.patch(
            self.url_detail,
            data={
                "description": "comment1 updated"
            }
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )

    def test_delete(self):
        contributors_count = self.project1.contributors.all().count()
        response = self.client.delete(
            self.url_detail,
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json(),
            self.get_response_not_permited()
        )
        self.assertEqual(
            self.project1.contributors.all().count(),
            contributors_count
        )


class TestCommentAsNotContributor(AppAPITestCase):
    url_list = reverse_lazy('project-issue-comment-list', args=(1, 1))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.access_token = cls.client.post(
            cls.get_token_url,
            {
                "username": "user3",
                "password": "wxcv1234"
            }
        ).data.get("access")
        cls.url_detail = reverse_lazy(
            'project-issue-comment-detail',
            args=(1, 1, cls.comment1.id)
        )

    def setUp(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

    def test_list(self):
        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )

    def test_detail(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.json(),
            self.get_response_not_found()
        )
