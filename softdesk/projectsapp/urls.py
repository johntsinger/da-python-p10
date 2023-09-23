from django.urls import path, include
from rest_framework_nested import routers
from projectsapp.views import (
    ProjectViewSet,
    IssueViewSet
)


router = routers.SimpleRouter()
router.register(
    r'project',
    ProjectViewSet,
    basename='project'
)

project_router = routers.NestedSimpleRouter(
    router,
    r'project',
    lookup='project'
)
project_router.register(
    r'issues',
    IssueViewSet,
    basename='project-issue'
)

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/', include(project_router.urls)),
]
