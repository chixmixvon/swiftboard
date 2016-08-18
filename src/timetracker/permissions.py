from rest_framework import permissions

from . import mixins


SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']

UPDATE_METHODS = ['DELETE', 'PATCH', 'PUT']


class ProjectAdminPermission(mixins.TimeTrackerMixin, permissions.BasePermission):
    """Check if user is project admin
    """

    def has_permission(self, request, view):
        """Allow user to access project member
        """
        project_pk = view.kwargs.get('project_pk')
        user_id = request.user.id
        return True if self.user_permission(project_pk, user_id, 1) or self.user_permission(project_pk, user_id, 2) else False


class ProjectMemberPermission(mixins.TimeTrackerMixin, permissions.BasePermission):

    def has_permission(self, request, view):
        """Check if user is a member
        """

        project_pk = view.kwargs.get('project_pk')
        user_id = request.user.id
        return True if self.user_permission(project_pk, user_id) else False
