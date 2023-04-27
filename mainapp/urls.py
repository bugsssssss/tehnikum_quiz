from rest_framework import routers
from .views import *
from django.http import HttpResponse
from django.urls import path

routers = routers.DefaultRouter()
routers.register('questions', QuestionViewSet)
routers.register('quizzes', QuizViewSet)
routers.register('answers', AnswersViewSet)
routers.register('temp-users', TempUsersViewSet)
routers.register('user-answers', UserAnswersViewSet)
# routers.register('get-user', UserDetailViewSet)


urlpatterns = [
    # path('', home, name='home'),
    path('bot-users/', BotUsersList.as_view(), name='bot-users'),
    path('bot-users/<int:pk>/', BotUsersDetail.as_view(), name='bot-users-detail'),
    path('questions/<int:pk>/', QuestionDetail.as_view(), name='question-detail'),
    path('answers/<int:pk>/', AnswersDetail.as_view(), name='answers-detail'),
    path('temp-users/<int:pk>/', TempUsersDetail.as_view(),
         name='temp-users-detail'),
    path('get-user', GetUserDetail.as_view(), name='get-user-detail'),
    path('get-user/<int:pk>/',
         GetUserDetail.as_view(), name='get-user-detail'),
    path('correct-answers/', CorrectAnswers.as_view(), name='correct-answers'),
]
urlpatterns += routers.urls
