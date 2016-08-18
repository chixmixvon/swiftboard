from django.conf.urls import url, include

from rest_framework_nested import routers as nested_routers

from . import views

# /projects/
project_router = nested_routers.SimpleRouter()
project_router.register(r'projects', views.ProjectViewSet)

# /projects/<project_pk>/members/
member_router = nested_routers.NestedSimpleRouter(project_router, r'projects', lookup='project')
member_router.register(r'members', views.ProjectMemberViewSet, base_name='members')

# /projects/<project_pk>/tasks/
task_router = nested_routers.NestedSimpleRouter(project_router, r'projects', lookup='project')
task_router.register(r'tasks', views.TaskViewSet, base_name='project_task')

# /projects/<project_pk>/tasks/<task_pk>/comments/
task_comment_router = nested_routers.NestedSimpleRouter(task_router, r'tasks', lookup='task')
task_comment_router.register(r'comments', views.TaskCommentViewSet, base_name='project_task_comment')

urlpatterns = [
        # projects
        url(r'^', include(project_router.urls)),
        url(r'^', include(member_router.urls)),
        url(r'^', include(task_router.urls)),
        url(r'^', include(task_comment_router.urls)),

    ]
