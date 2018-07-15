from django.urls import path
from forum import views

app_name = 'class_join'

urlpatterns = [
    path('join/', views.join_class, name='join')
]
