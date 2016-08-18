from django.contrib import admin

from . import models


class ProjectMemberInline(admin.TabularInline):
    model = models.ProjectMember


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created', 'user')
    list_filter = ('user',)
    raw_id_fields = ('user',)
    inlines = (ProjectMemberInline,)

admin.site.register(models.Project, ProjectAdmin)


class TaskLogInline(admin.TabularInline):
    model = models.TaskLog
    readonly_fields = ('start', 'end')


class TaskCommentInline(admin.TabularInline):
    model = models.TaskComment


class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'assignee', 'status', 'project')
    raw_id_fields = ('assignee', 'project')
    inlines = (TaskLogInline, TaskCommentInline)
    list_filter = ('status', 'project', 'assignee')

admin.site.register(models.Task, TaskAdmin)
