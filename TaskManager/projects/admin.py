from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1
    raw_id_fields = ('user_id',)
    fields = ('user_id', 'get_username', 'user_role')
    readonly_fields = ('get_username',)

    def get_username(self, obj):
        return obj.user_id.username if obj.user_id else '-'

    get_username.short_description = 'Username'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = (ProjectMemberInline,)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'user_id', 'get_username', 'user_role')
    list_select_related = ('user_id',)
    list_filter = ('user_role',)

    def get_username(self, obj):
        return obj.user_id.username

    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user_id__username'
