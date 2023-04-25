from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def get_queryset(self):
        queryset = Question.objects.all()
        quiz_id = self.request.query_params.get('quiz_id', None)

        if quiz_id is not None:
            print(quiz_id)
            queryset = queryset.filter(quiz__id=quiz_id)

        return queryset


class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class BotUsersList(generics.ListCreateAPIView):
    queryset = BotUsers.objects.all()
    serializer_class = BotUsersSerializer

    def get_queryset(self):
        queryset = BotUsers.objects.all()
        user_id = self.request.query_params.get('id', None)
        if user_id:
            queryset = queryset.filter(id=user_id)

        return queryset


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class BotUsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BotUsers.objects.all()
    serializer_class = BotUsersSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def get_queryset(self):
        queryset = Answer.objects.all()
        answer_id = self.request.query_params.get('answer-id', None)
        is_correct = self.request.query_params.get('is-correct', None)

        # if answer_id and is_correct:
        #     queryset = queryset.filter(id=answer_id, is_correct=is_correct)
        #     return queryset

        if answer_id:
            queryset = queryset.filter(id=answer_id)
            return queryset

        # if is_correct:
        #     queryset = queryset.filter(is_correct=is_correct)
        #     return queryset

        return queryset


class AnswersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer


def home(request):
    form = BotUsersForm()
    if request.method == 'POST':
        print(request.POST)
        form = BotUsersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('https://t.me/tehnikum_promo_bot')
    context = {
        'form': form
    }
    return render(request, 'index.html', context)


class TempUsersViewSet(viewsets.ModelViewSet):
    queryset = TempUser.objects.all()
    serializer_class = TempUserSerializer

    def get_queryset(self):
        queryset = TempUser.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset


class TempUsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = TempUser.objects.all()
    serializer_class = TempUserSerializer
