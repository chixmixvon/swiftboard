from django.db import models
from django.contrib.auth.models import User


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Project(BaseModel):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=200, blank=False, null=False)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ProjectMember(BaseModel):
    PERMISSION = (
                    (1, 'Admin'),
                    (2, 'Project Manager'),
                    (3, 'Developer'),
                    (4, 'Viewer'),
                )

    project = models.ForeignKey(Project, related_name='project_member')
    user = models.ForeignKey(User, related_name='member', blank=False, null=False)
    permission = models.IntegerField(choices=PERMISSION, default=1)

    def __str__(self):
        return '{} - {} - {}'.format(self.project, self.user.email, self.permission)

    class Meta:
        unique_together = ('project', 'user')


class Task(BaseModel):
    STATUS = (
              (0, 'Backlog'),
              (1, 'Todo'),
              (2, 'In Progress'),
              (3, 'Resolved'),
              (4, 'Closed'),
        )

    project = models.ForeignKey(Project, related_name='task_project')
    title = models.CharField(max_length=500, blank=False, null=False)
    description = models.TextField(blank=True)
    assignee = models.ForeignKey(User, blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    user = models.ForeignKey(User, blank=True, related_name='creator')
    order = models.IntegerField(default=0, blank=True, null=True)


class TaskLog(BaseModel):
    task = models.ForeignKey(Task, related_name='task_log')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)


class TaskComment(BaseModel):
    task = models.ForeignKey(Task, related_name='task_comment')
    comment = models.TextField(blank=True)
    comment_by = models.ForeignKey(User)
