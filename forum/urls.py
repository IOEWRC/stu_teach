from django.urls import path
from forum import views

app_name = 'forum'

urlpatterns = [
    path('', views.home, name='home'),
    path('classes/', views.ClassListView.as_view(), name='class_list'),
    path('classes/<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    # path('classes/create/', views.ClassCreateView.as_view(), name='class_create'),
    path('classes/delete/<int:pk>/', views.ClassDeleteView.as_view(), name='class_delete'),
    path('classes/update/<int:pk>/', views.ClassUpdateView.as_view(), name='class_update'),
    # path('classes/questions/<int:pk>/', views.QuestionCreateView.as_view(), name='question_create'),
    path('classes/question/detail/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    path('classes/question/update/<int:pk>/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('classes/question/delete/<int:pk>/', views.QuestionDeleteView.as_view(), name='question_delete'),
    # path('classes/answer/<int:pk>/', views.AnswerCreateView.as_view(), name="answer_create"),
    path('classes/answer/<int:pk>/delete/', views.AnswerDeleteView.as_view(), name="answer_delete"),
    path('classes/answer/<int:pk>/update/', views.AnswerUpdateView.as_view(), name="answer_update"),
    path('classes/answer/<int:pk>/detail/', views.AnswerDetailView.as_view(), name="answer_detail"),
    # path('classes/answer/reply/<int:pk>/', views.ReplyCreateView.as_view(), name="reply_create"),
    path('classes/answer/reply/<int:pk>/delete/', views.ReplyDeleteView.as_view(), name="reply_delete"),
    path('classes/answer/reply/<int:pk>/update/', views.ReplyUpdateView.as_view(), name="reply_update"),
    # path('class/join/', views.join_class, name='join')
]
