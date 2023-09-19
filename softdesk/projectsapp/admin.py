from django.contrib import admin
from projectsapp.models import (
    Contributor,
    Project,
    Issue,
    Comment
)


admin.site.register(Contributor)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
