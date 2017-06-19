from django.contrib import admin
from attendance.models import Session, Swipe, Key, Project, ProjectSeparation, Holiday, Profile, Contract


class ProjectSeparationInline(admin.TabularInline):
    model = ProjectSeparation


class SwipeInline(admin.TabularInline):
    model = Swipe
    fields = ('datetime', 'user', 'swipe_type', 'source', )
    readonly_fields = ('datetime', 'user', 'swipe_type', 'source')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    inlines = [
        SwipeInline,
        ProjectSeparationInline,
    ]
    list_select_related = ['user']
    readonly_fields = ('user', 'modified', 'duration')

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Key)
class KeyAdmin(admin.ModelAdmin):
    list_select_related = ['user']


@admin.register(Swipe)
class SwipeAdmin(admin.ModelAdmin):
    list_select_related = ['user']
    fields = ('datetime', 'user', 'swipe_type', 'source')

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Project)
admin.site.register(Holiday)
admin.site.register(Profile)
admin.site.register(Contract)
