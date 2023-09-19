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
        return Project.objects.filter(
            contributors__user_id=self.request.user.id
        )

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
        project = serializer.save()
        contributor = Contributor.objects.create(
            user=self.request.user,
            role='AUTHOR'
        )
        contributor.save()
        project.contributors.set([contributor])
