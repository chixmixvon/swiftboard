from django.utils import timezone
from django.contrib.auth.models import User

from . import models


class TimeTrackerMixin(object):

    def get_task(self, task_id):
        """Return task object
        """
        return models.Task.objects.get(id=task_id)

    def get_user(self, user_id):
        """Return user object
        """
        return User.objects.get(id=user_id)

    def get_project(self, project_id):
        """Return probject object
        """
        return models.Project.objects.get(id=project_id)

    def task_log(self, task_id, user_id, log):
        """Start/End to log task

        Details:
        * User unable to logged if not assigned to the task
        """
        user = self.get_user(user_id)
        task = self.get_task(task_id)

        if task.assignee == user:
            if log == 'start':
                task_log = models.TaskLog(
                                          task=task,
                                          start=timezone.now()
                                    )
                task_log.save()

                # Set the task automatically to in progress
                task.status = 2
                task.save()
                return task_log
            elif log == 'end':
                task_log = models.TaskLog.objects.get(task=task)
                task_log.end = timezone.now()
                task_log.save()
                return task_log

        return None

    def task_active(self, user_id):
        """Return active task
        """
        user = self.get_user(user_id)

        if models.TaskLog.objects.filter(task__assignee=user, end=None):
            return True

        return False

    def user_permission(self, project_id, user_id, permission=None):
        """Check user permission
        """
        member = models.ProjectMember.objects.filter(project__id=project_id, user__id=user_id)

        if permission:
            member = member.filter(permission=permission)

        return member
