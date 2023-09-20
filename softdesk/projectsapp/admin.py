from django.contrib import admin
from projectsapp.models import (
    Contributor,
    Project,
    Issue,
    Comment
)


class ContributorInline(admin.TabularInline):
    model = Contributor
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ContributorInline]

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        form.instance.contributors.add(
            form.instance.author,
            through_defaults={
                'role': 'AUTHOR'
            }
        )


admin.site.register(Contributor)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Issue)
admin.site.register(Comment)
