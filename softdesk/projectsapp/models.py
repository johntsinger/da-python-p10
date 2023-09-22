import uuid
from django.conf import settings
from django.db import models


class Project(models.Model):
    BACKEND = 'BACKEND'
    FRONTEND = 'FRONTEND'
    iOS = 'iOS'
    ANDROID = 'ANDROID'

    TYPE_CHOICES = [
        (BACKEND, 'BACKEND'),
        (FRONTEND, 'FRONTEND'),
        (iOS, 'iOS'),
        (ANDROID, 'ANDROID')
    ]

    name = models.CharField(
        max_length=128
    )
    description = models.CharField(
        max_length=4096
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='projects_created'
    )
    contributors = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through='Contributor',
        related_name='projects'
    )
    type = models.CharField(
        max_length=8,
        choices=TYPE_CHOICES,
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Add author to contributor if created"""
        if not self.pk:
            super().save(*args, **kwargs)
            self.contributors.add(
                self.author,
                through_defaults={
                    'role': 'AUTHOR'
                }
            )
        else:
            super().save(*args, **kwargs)


class Contributor(models.Model):
    AUTHOR = 'AUTHOR'
    CONTRIBUTOR = 'CONTRIBUTOR'

    ROLE_CHOICES = [
        (AUTHOR, 'AUTHOR'),
        (CONTRIBUTOR, 'CONTRIBUTOR')
    ]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,

    )
    role = models.CharField(
        max_length=11,
        choices=ROLE_CHOICES,
        default=CONTRIBUTOR
    )

    class Meta:
        unique_together = ('user', 'project')


class Issue(models.Model):
    # Priority
    LOW = 'LOW'
    MEDIUM = 'MEDIUM'
    HIGH = 'HIGH'

    PRIORITY_CHOICES = [
        (LOW, 'LOW'),
        (MEDIUM, 'MEDIUM'),
        (HIGH, 'HIGH')
    ]

    # Type
    BUG = 'BUG'
    FEATURE = 'FEATURE'
    TASK = 'TASK'

    TAG_CHOICES = [
        (BUG, 'BUG'),
        (FEATURE, 'FEATURE'),
        (TASK, 'TASK')
    ]

    # Status
    TO_DO = 'To Do'
    IN_PROGRESS = 'In Progress'
    FINISHED = 'Finished'

    STATUS_CHOICES = [
        (TO_DO, 'To Do'),
        (IN_PROGRESS, 'In Progress'),
        (FINISHED, 'Finished')
    ]

    name = models.CharField(
        max_length=128
    )
    description = models.CharField(
        max_length=4096
    )
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default=LOW
    )
    tag = models.CharField(
        max_length=7,
        choices=TAG_CHOICES,
    )
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default=TO_DO
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name='issues'
    )
    assigned_to = models.ForeignKey(
        to=Contributor,
        on_delete=models.CASCADE,
        related_name='issues_assigned',
        blank=True,
        null=True
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='issues_created'
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True,
        unique=True,
        editable=False,
        default=uuid.uuid4,
    )
    description = models.CharField(
        max_length=4096
    )
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments_created'
    )
    time_created = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.description
