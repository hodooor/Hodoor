from django.contrib import admin
from attendance.models import Session, Swipe, Key, Project, ProjectSeparation
from django.forms import ModelForm

class SwipeInline(admin.TabularInline):
    model = Swipe

class ProjectSeparationInline(admin.TabularInline):
    model = ProjectSeparation

class SessionAdmin(admin.ModelAdmin):
    inlines = [
            SwipeInline,
            ProjectSeparationInline,
            ]



admin.site.register(Session, SessionAdmin)
admin.site.register(Swipe)
admin.site.register(Key)
admin.site.register(Project)
admin.site.register(ProjectSeparation)
