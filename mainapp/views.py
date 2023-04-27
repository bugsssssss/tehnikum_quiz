from django.shortcuts import render, redirect
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from .forms import *
from rest_framework import status
import requests


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

    def get_queryset(self):
        queryset = Quiz.objects.all()
        category_id = self.request.query_params.get('category_id', None)
        if category_id:
            queryset = queryset.filter(category__id=category_id)
        return queryset


class BotUsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BotUsers.objects.all()
    serializer_class = BotUsersSerializer

    def update(self, request, *args, **kwargs):
        # Get the instance to be updated
        instance = self.get_object()
        print('instance: ', instance)
        # Create a dictionary with the new data to be updated
        data = {
            "category_id": request.data.get(
                "category_id"),
            "is_verified": request.data.get(
                "is_verified"),
        }
        if data['is_verified'] == None:
            data['is_verified'] = False

        # Create an instance of the serializer with the new data and the partial flag
        serializer = self.get_serializer(instance, data=data, partial=True)

        # Check if the serializer is valid and save the changes to the database
        if serializer.is_valid():
            serializer.save()
            return Response('success', status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class UserAnswersViewSet(viewsets.ModelViewSet):
    queryset = UserAnswers.objects.all()
    serializer_class = UserAnswersSerializer

    # def get_queryset(self):
    #     queryset = UserAnswers.objects.all()
    #     user_id = self.request.query_params.get('user_id', None)
    #     question_id = self.request.query_params.get('question_id', None)
    #     if user_id:
    #         queryset = queryset.filter(user_id=user_id)
    #     if question_id:
    #         queryset = queryset.filter(question_id=question_id)
    #     return queryset

    def list(self, request):
        user_id = self.request.query_params.get('user_id', None)
        question_id = self.request.query_params.get('question_id', None)

        if user_id and question_id:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(
                user_id=user_id, question_id=question_id)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the data to the database
            self.perform_create(serializer)
            # Return a response with the created data
            user_data = {
                'id': serializer.data['id'],
                'user_id': serializer.data['user_id'],
                'question_id': serializer.data['question_id'],
                'answer_id': serializer.data['answer_id'],
                'is_correct': 'test',
            }
            is_correct = Answer.objects.get(
                id=serializer.data['answer_id']).is_correct
            answers = Question.objects.get(
                id=serializer.data['question_id']).answers.all()
            correct_answer = None
            for i in answers:
                if i.is_correct:
                    correct_answer = i.id
            response = {
                'is_correct': is_correct,
                'answer_id': correct_answer,
            }
            return Response(response, status=status.HTTP_201_CREATED)
        else:
            # Return a response with the errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = UserAnswers.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset


# class UserDetailViewSet(viewsets.ModelViewSet):
#     queryset = UserDetail.objects.all()
#     serializer_class = UserDetailSerializer

#     # def create(self, request, *args, **kwargs):
#     #     serializer = self.get_serializer(data=request.data)
#     #     if serializer.is_valid():
#     #         # Save the data to the database
#     #         self.perform_create(serializer)
#     #         # Return a response with the created data

#     #         return Response(user_data, status=status.HTTP_201_CREATED)
#     #     else:
#     #         # Return a response with the errors
#     #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_queryset(self):
#         queryset = UserDetail.objects.all()
#         user_id = self.request.query_params.get('user_id', None)
#         if user_id:
#             queryset = queryset.filter(user_id=user_id)
#         return queryset


# class GetUserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = GetUser.objects.all()
#     serializer_class = GetUserDetailSerializer
#     print(queryset)

    # def update(self, request, *args, **kwargs):
    #     # Get the instance to be updated
    #     instance = self.get_object()

    #     # Create a dictionary with the new data to be updated
    #     data = {"user_id": request.data.get("user_id")}

    #     # Create an instance of the serializer with the new data and the partial flag
    #     serializer = self.get_serializer(instance, data=data, partial=True)

    #     # Check if the serializer is valid and save the changes to the database
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response('success', status=status.HTTP_200_OK)
    #     else:
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserDetail(APIView):

    def get(self, request):
        user_id = int(request.query_params.get('user_id', None))
        # category_id = int(request.query_params.get('category_id', None))

        user = None
        try:
            user = requests.get(
                f'https://p-api2.tehnikum.school/api/bot-users/?id={user_id}').json()
        except:
            pass
        print(user)
        category_id = user[0]['category_id']
        print(category_id)
        if category_id:
            required_questions = requests.get(
                f'https://p-api2.tehnikum.school/api/quizzes/?category_id={category_id}').json()[0]['questions']
            questions = []
            for i in required_questions:
                correct_answer = None
                answers = i['answers']
                for j in answers:
                    if j['is_correct']:
                        correct_answer = j['answer_id']
                question_data = {
                    'question_id': i['question_id'],
                    'question_status': 'wait',
                    'selected_answer': 'none',
                    'correct_answer': correct_answer,
                    # 'answers': i['answers'],
                }
                selected_answer = requests.get(
                    f'http://p-api2.tehnikum.school/api/user-answers/?user_id={user[0]["id"]}&question_id={question_data["question_id"]}').json()
                question_data['selected_answer'] = selected_answer
                if selected_answer:
                    question_data['selected_answer'] = selected_answer[0]['answer_id']
                    selected_answer = selected_answer[0]['answer_id']
                    if selected_answer == correct_answer:
                        question_data['question_status'] = 'correct'
                    else:
                        question_data['question_status'] = 'incorrect'
                else:
                    question_data['selected_answer'] = None
                questions.append(question_data)
            print(question_data)
        else:
            questions = None

        data = {
            'user_id': user[0]['id'],
            'first_name': user[0]['first_name'],
            'category_id': category_id,
            'questions': questions,
        }

        return Response(data)


class CorrectAnswers(APIView):

    def get(self, request):
        user_id = int(request.query_params.get('user_id', None))

        user = requests.get(
            f'https://p-api2.tehnikum.school/api/bot-users/?id={user_id}').json()

        if user:
            user_id = user[0]['id']
            user_anwers = requests.get(
                f'http://p-api2.tehnikum.school/api/user-answers/?user_id={user_id}').json()
            correct_answers = 0
            for i in user_anwers:
                if i['is_correct']:
                    correct_answers += 1
            print(correct_answers)
            discount = '0%'
            if correct_answers == 5:
                discount = '40%'
            elif correct_answers == 4:
                discount = '32%'
            elif correct_answers == 3:
                discount = '24%'
            elif correct_answers == 2:
                discount = '16%'
            elif correct_answers == 1:
                discount = '8%'
            else:
                discount = '0%'
            return Response({
                'user_id': user_id,
                'correct_answers': correct_answers,
                'discount': discount,
            })

        else:
            user_id = None
