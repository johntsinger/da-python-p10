from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from projectsapp.models import (
    Project,
    Issue,
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
    IsContributor,
    IsProjectCreator
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
        if self.action == 'list':
            return Project.objects.all().select_related('author').only(
                'id',
                'name',
                'description',
                'type',
                'author__username'
            )
        return Project.objects.annotate(
            open_issues_count=Count(
                'issues',
                filter=~Q(issues__status='Finished')
            ),
            closed_issues_count=Count(
                'issues',
                filter=Q(issues__status='Finished')
            )
        ).select_related('author')

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


class ContributorViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = ContributorListSerializer
    detail_serializer_class = ContributorDetailSerializer
    add_serilaizer_class = AddContributorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'delete', 'head', 'options']

    def get_queryset(self):
        return get_object_or_404(
            self.request.user.projects,
            pk=self.kwargs['project_pk']
        ).contributor_set.select_related('user')

    def get_serializer_class(self):
        if self.action == 'create':
            return self.add_serilaizer_class
        else:
            return super().get_serializer_class()

    def get_permissions(self):
        """
        Instantiates and returns the list of
        permissions that this view requires.
        """
        if self.action in (
            'destroy',
            'update',
            'partial_update',
            'create'
        ):
            permission_classes = (
                self.permission_classes + [IsProjectCreator]
            )
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def destroy(self, request, *args, **kwargs):
        contributor = self.get_object()
        if contributor.pk == contributor.project.author.pk:
            return Response(
                {
                    'detail':
                    'You cannot remove the author from the contributors.'
                    ' Delete the project instead.'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        self.perform_destroy(contributor)
        return Response(
            {"detail: Contributor removed"},
            status=status.HTTP_200_OK
        )

    def perform_create(self, serializer):
        serializer.save(
            project=Project.objects.get(pk=self.kwargs['project_pk'])
        )


class IssueViewSet(MultipleSerializerMixin, ModelViewSet):
    serializer_class = IssueListSerializer
    detail_serializer_class = IssueDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(
            self.request.user.projects,
            pk=self.kwargs['project_pk']
        ).issues.annotate(
            comments_count=Count('comments')
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
            permission_classes = (
                self.permission_classes + [IsAuthor | IsProjectCreator]
            )
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            project=Project.objects.get(pk=self.kwargs['project_pk'])
        )


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(
            get_object_or_404(
                self.request.user.projects.select_related('author'),
                pk=self.kwargs['project_pk']
            ).issues,
            pk=self.kwargs['issue_pk']
        ).comments.select_related('author')

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
            permission_classes = (
                self.permission_classes + [IsAuthor | IsProjectCreator]
            )
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            issue=Issue.objects.get(pk=self.kwargs['issue_pk'])
        )
