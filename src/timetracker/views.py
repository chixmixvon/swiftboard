import logging

from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response

from . import models
from . import serializers
from . import permissions
from . import mixins

logger = logging.getLogger('django')


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer

    def get_querset(self, *args, **kwargs):
        queryset = self.queryset.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializers, *args, **kwargs):
        serializers.save(user=self.request.user)

    def perform_update(self, serializers, *args, **kwargs):
        serializers.save(user=self.request.user)


class ProjectMemberViewSet(mixins.TimeTrackerMixin, viewsets.ModelViewSet):
    queryset = models.ProjectMember.objects.all()
    serializer_class = serializers.ProjectMemberSerializer
    permission_classes = (permissions.ProjectAdminPermission,)

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(project__id=self.kwargs['project_pk'])
        return queryset

    def perform_create(self, serializers, *args, **kwargs):
        serializers.save(project=self.get_project(self.kwargs['project_pk']))

    def perform_update(self, serializers, *args, **kwargs):
        serializers.save(project=self.get_project(self.kwargs['project_pk']))


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = (permissions.ProjectMemberPermission,)

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(project__id=self.kwargs['project_pk'])
        return queryset

    def perform_create(self, serializers, *args, **kwargs):
        serializers.save(user=self.request.user)

    def perform_update(self, serializers, *args, **kwargs):
        serializers.save(user=self.request.user)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = models.TaskComment.objects.all()
    serializer_class = serializers.TaskCommentSerializer
    permission_classes = (permissions.ProjectMemberPermission,)

    def get_queryset(self, *args, **kwargs):
        queryset = self.queryset.filter(task__id=self.kwargs['task_pk'], task__project__id=self.kwargs['project_pk'])
        return queryset

    def perform_create(self, serializers):
        serializers.save(comment_by=self.request.user)

    def perform_update(self, serializers):
        serializers.save(comment_by=self.request.user)

    def destroy(self, request):
        """Allow user to delete created comment
        """
        instance = self.get_object()

        if instance.comment_by == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)
