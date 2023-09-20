from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from projectsapp.models import (
    Contributor,
    Project,
    Issue,
    Comment
)


class FieldMixin:
    """Get all fields. This avoids writing each field manually.
    Use '__all__' in serailizer and add the extra_fields attribute
    along with the other fields you want to pass.
    (extra_fields must be a list)"""

    def get_field_names(self, declared_fields, info):
        extra_fields = getattr(self.Meta, 'extra_fields', None)
        fields = super().get_field_names(declared_fields, info)
        if extra_fields:
            return fields + extra_fields
        else:
            return fields


class ContributorListSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'role'
        ]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class IssueListSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = '__all__'


class IssueDetailSerializer(FieldMixin, ModelSerializer):
    comments = SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'
        extra_fields = ['comments']

    def get_comments(self, instance):
        queryset = instance.comments.all()
        serializer = CommentSerializer(queryset, many=True)
        return serializer.data


class ProjectListSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'


class ProjectDetailSerailizer(FieldMixin, ModelSerializer):
    issues = SerializerMethodField()
    contributors = SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['issues', 'contributors']

    def get_issues(self, instance):
        queryset = instance.issues.all()
        serializer = IssueListSerializer(queryset, many=True)
        return serializer.data

    def get_contributors(self, instance):
        queryset = instance.contributors.all()
        serializer = ContributorListSerializer(queryset, many=True)
        return serializer.data


class ContributorDetailSerializer(ModelSerializer):
    projects = SerializerMethodField()

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'role',
            'projects'
        ]

    def get_projects(self, instance):
        queryset = instance.project
        serializer = ProjectListSerializer(queryset, many=True)
        return serializer.data