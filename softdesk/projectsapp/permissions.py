from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from projectsapp.models import (
    Project,
)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user == obj.author
        )


class IsDataOwner(BasePermission):
    def has_permission(self, request, view):
        if 'user' in request.data:
            return (
                request.user.id == int(request.data['user'])
            )
        return True


class IsContributor(BasePermission):
    def has_permission(self, request, view):
        if 'project_pk' in view.kwargs:
            project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
            return request.user in project.contributors.all()
        return True

    def has_object_permission(self, request, view, obj):
        if 'project_pk' not in view.kwargs:
            return request.user in obj.contributors.all()
        return True
