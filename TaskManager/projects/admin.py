from django.contrib import admin
from .models import Project, ProjectMember


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1
    raw_id_fields = ('user',)
    fields = ('user', 'get_username', 'user_role')
    readonly_fields = ('get_username',)

    def get_username(self, obj):
        return obj.user.username if obj.user else '-'  # Используем obj.user вместо obj.user_id

    get_username.short_description = 'Username'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = (ProjectMemberInline,)


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'get_username', 'user_role')
    list_select_related = ('user',)  # Раскомментируйте для оптимизации запросов
    list_filter = ('user_role',)

    def get_username(self, obj):
        return obj.user.username  # Используем obj.user вместо obj.user_id

    get_username.short_description = 'Username'
    get_username.admin_order_field = 'user__username'  # Исправлено на user__username