from rest_framework import routers
from django.urls import path, include
from projectsapp.views import (
    ProjectViewSet,
)


router = routers.SimpleRouter()
router.register('project', ProjectViewSet, basename='project')

urlpatterns = [
    path('api/', include(router.urls))
]
