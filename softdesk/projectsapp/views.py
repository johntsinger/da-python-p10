from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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
from projectsapp.permissions import (
    IsAuthor,
    IsDataOwner,
    IsContributor
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
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        return self.request.user.projects.all()

    def get_permissions(self):
        """
        Instantiates and returns the list of
        permissions that this view requires.
        """
        if self.action in (
            'destroy',
            'update',
            'partial_update',
            'add_contributor'
        ):
            permission_classes = self.permission_classes + [IsAuthor]
        elif self.action == 'remove_contibutor':
            permission_classes = (
                self.permission_classes + [IsDataOwner | IsAuthor]
            )
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        project.contributors.add(
            project.author,
            through_defaults={
                'role': 'AUTHOR'
            }
        )

    @action(
        methods=['post'],
        detail=True,
        url_path='add-contributor',
        url_name='add_contributor',
        serializer_class=AddContributorSerializer
    )
    def add_contributor(self, request, pk=None):
        serializer = self.serializer_class(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save(project=self.get_object())
            return Response(
                {'status': 'Contributor added.'}
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
                    'You cannot remove the author from the contributors.'
                    ' Delete the project instead.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not project.contributors.filter(
            id=int(request.data['user'])
        ).exists():
            return Response(
                {
                    "user": [
                        f"Invalid pk {request.data['user']}"
                        " - Contributor does not exist."
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.get_object().contributors.remove(
            request.data['user']
        )
        return Response(
            {'status': 'Contributor removed.'}
        )


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated, IsContributor]

    def get_queryset(self):
        return Issue.objects.filter(
            project=self.kwargs['project_pk']
        )

    def get_permissions(self):
        """
        Instantiates and returns the list of
        permissions that this view requires.
        """
        if self.action in (
            'destroy',
            'update',
            'partial_update',
        ):
            permission_classes = self.permission_classes + [IsAuthor]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            project=Project.objects.get(pk=self.kwargs['project_pk'])
        )
