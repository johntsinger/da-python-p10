from rest_framework import status
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from projectsapp.models import (
    Contributor,
    Project,
    Issue,
    Comment
)
from projectsapp.serializers import (
    ContributorListSerializer,
    ContributorDetailSerializer,
    ProjectListSerializer,
    ProjectDetailSerailizer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentSerializer
)


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if (
            self.action == 'retrieve'
            and self.detail_serializer_class is not None
        ):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ProjectListSerializer
    detail_serializer_class = ProjectDetailSerailizer

    def get_queryset(self):
        return self.request.user.projects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        project.contributors.add(
            project.author,
            through_defaults={
                'role': 'AUTHOR'
            }
        )
        return project
