from django.urls import path
from .views import Home, AssignmentView, TaskView

app_name = 'assignment'


urlpatterns = [
    path('<int:pk>/', Home.as_view(), name='assignment_home'),
    path('task/', TaskView.as_view(), name='task'),
    path('assign/', AssignmentView.as_view(), name='assign'),
]
