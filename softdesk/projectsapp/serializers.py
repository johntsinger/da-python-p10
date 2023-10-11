from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
    StringRelatedField,
    SlugRelatedField,
    ReadOnlyField,
)
from projectsapp.models import (
    Contributor,
    Project,
    Issue,
    Comment
)
from authentication.serializers import UserSerializer


User = get_user_model()


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
    user = StringRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'role'
        ]


class CommentSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    issue = StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ContributorSlugRelatedField(SlugRelatedField):
    def get_queryset(self):
        return User.objects.filter(
            projects=self.context['view'].kwargs['project_pk']
        )

    def to_representation(self, value):
        if isinstance(value, Contributor):
            return value.user.username
        else:
            return value


class IssueListSerializer(ModelSerializer):
    author = StringRelatedField(read_only=True)
    assigned_to = ContributorSlugRelatedField(
        slug_field='username',
        error_messages={
            'does_not_exist':
                ('Contributor object with user_{slug_name}={value} '
                 'is not a contributor of this project.')
        },
        required=False
    )

    class Meta:
        model = Issue
        exclude = ('time_created', 'project')
        extra_kwargs = {
            'description': {'write_only': True},
            'tag': {'write_only': True},
            'status': {'write_only': True}
        }

    def validate_assigned_to(self, value):
        return Contributor.objects.get(
            project_id=self.context['view'].kwargs['project_pk'],
            user=value,
        )


class IssueDetailSerializer(FieldMixin, ModelSerializer):
    author = StringRelatedField(read_only=True)
    project = StringRelatedField(read_only=True)
    assigned_to = ContributorSlugRelatedField(slug_field='username')
    comments_count = SerializerMethodField()

    class Meta:
        model = Issue
        fields = '__all__'
        extra_fields = ['comments_count']

    def get_comments_count(self, instance):
        return instance.comments_count


class ProjectListSerializer(ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Project
        exclude = ('time_created', 'contributors')
        extra_kwargs = {
            'description': {'write_only': True}
        }


class ProjectDetailSerailizer(FieldMixin, ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    contributors = ContributorListSerializer(
        source='contributor_set',
        many=True
    )
    open_issues_count = SerializerMethodField()
    closed_issues_count = SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'
        extra_fields = ['open_issues_count', 'closed_issues_count']

    def get_open_issues_count(self, instance):
        return instance.open_issues_count

    def get_closed_issues_count(self, instance):
        return instance.closed_issues_count


class ContributorDetailSerializer(ModelSerializer):
    user = UserSerializer()
    project = StringRelatedField(read_only=True)

    class Meta:
        model = Contributor
        fields = '__all__'


class AddContributorSerializer(ModelSerializer):
    user = SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        error_messages={
            "does_not_exist":
                "User object with {slug_name}={value} does not exist."
        }
    )
    id = ReadOnlyField()
    role = ReadOnlyField()
    project = StringRelatedField()

    class Meta:
        model = Contributor
        fields = [
            'id',
            'user',
            'role',
            'project'
        ]

    def create(self, validated_data):
        if Contributor.objects.filter(
            **validated_data
        ).exists():
            raise ValidationError(
                {
                    'unique constraint failed':
                        [
                            "This contributor already exists."
                        ]
                }
            )

        return super().create(validated_data)
