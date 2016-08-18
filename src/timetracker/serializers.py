from rest_framework import serializers
from django.contrib.auth.models import User

from . import models


class ProjectSerializer(serializers.ModelSerializer):

    user = serializers.CharField(required=False)

    class Meta:
        model = models.Project
        fields = '__all__'


class ProjectMemberSerializer(serializers.ModelSerializer):

    user = serializers.CharField(required=True)
    email = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_email(self, instance):
        """Return user email
        """
        return instance.user.email

    def get_user_id(self, instance):
        """Return user email
        """
        return instance.user.id

    def get_name(self, instance):
        """Return user email
        """

        if instance.user.first_name:
            return '{} {}'.format(instance.user.first_name, instance.user.last_name)
        return instance.user.email

    def validate_user(self, value):
        """Use email to add
        """
        try:
            user = User.objects.get(email=value)
            return user
        except User.DoesNotExist:
            user = User.objects.get(username=value)
            return user

    class Meta:
        model = models.ProjectMember
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):

    user = serializers.CharField(required=False)
    assignee_name = serializers.SerializerMethodField()
    assignee_initial = serializers.SerializerMethodField()

    def get_assignee_name(self, instance):
        """Return user email
        TODO: Add better function
        """

        try:
            if instance.assignee:
                return '{} {}'.format(instance.assignee.first_name, instance.assignee.last_name)
            return instance.assignee.email
        except AttributeError:
            return '?'

    def get_assignee_initial(self, instance):
        """Return user email
        TODO: Add better function
        """

        try:
            if instance.assignee:
                return '{} {}'.format(instance.assignee.first_name[0], instance.assignee.last_name[0])
            return instance.assignee.email[0]
        except AttributeError:
            return '?'

    class Meta:
        model = models.Task
        fields = '__all__'


class TaskLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskLog
        fields = '__all__'


class TaskCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.TaskComment
        fields = '__all__'
