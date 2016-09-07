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
    initial_avatar = serializers.SerializerMethodField()

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

    def get_initial_avatar(self, instance):
        """Return user email
        TODO: Add better function
        """

        try:
            if instance.user.first_name:
                return '{} {}'.format(instance.user.first_name[0], instance.user.last_name[0])
            return instance.user.email[0]
        except AttributeError:
            return '?'

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
