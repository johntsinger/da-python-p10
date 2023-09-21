from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
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
    CommentSerializer,
    AddContributorSerializer
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

    @action(
        methods=['post'],
        detail=True,
        url_path='add-contributor',
        url_name='add_contributor',
        serializer_class=AddContributorSerializer
    )
    def add_contibutor(self, request, pk=None):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(project=self.get_object())
            return Response(
                {'status': 'Contributor added'}
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['post'],
        detail=True,
        url_path='remove-contributor',
        url_name='remove_contributor',
        serializer_class=AddContributorSerializer
    )
    def remove_contibutor(self, request, pk=None):
        project = self.get_object()
        if project.author.id == int(request.data['user']):
            return Response(
                {
                    'detail':
                    'You cannot remove the author from the contributors'
                }
            )
        self.get_object().contributors.remove(
            request.data['user']
        )
        return Response(
            {'status': 'Contributor removed'}
        )
