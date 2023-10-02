from django.urls import path, include
from rest_framework_nested import routers
from projectsapp.views import (
    ProjectViewSet,
    IssueViewSet,
    ContributorViewSet,
    CommentViewSet,
)


router = routers.SimpleRouter()
router.register(
    r'projects',
    ProjectViewSet,
    basename='project'
)

project_router = routers.NestedSimpleRouter(
    router,
    r'projects',
    lookup='project'
)
project_router.register(
    r'issues',
    IssueViewSet,
    basename='project-issue'
)
project_router.register(
    r'contributors',
    ContributorViewSet,
    basename='project-contributor'
)

issue_router = routers.NestedSimpleRouter(
    project_router,
    r'issues',
    lookup='issue'
)
issue_router.register(
    r'comments',
    CommentViewSet,
    basename='project-issue-comment'
)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/', include(project_router.urls)),
    path(r'api/', include(issue_router.urls))
]
