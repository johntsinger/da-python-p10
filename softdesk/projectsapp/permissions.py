from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from projectsapp.models import (
    Project,
)


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.author.id


class IsProjectCreator(BasePermission):
    def has_permission(self, request, view):
        project = get_object_or_404(Project, pk=view.kwargs['project_pk'])
        return request.user == project.author


class IsContributor(BasePermission):
    message = "You must be a contributor to access this project."

    def has_object_permission(self, request, view, obj):
        if obj.author.can_be_contacted:
            self.message += (
                " Contact the project owner to "
                f"ask for an access : {obj.author.email}"
            )
        return request.user.id in obj.contributors.values_list('id', flat=True)
