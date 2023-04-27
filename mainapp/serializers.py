from rest_framework import serializers
from .models import *
from django.db.models import Q


class QuestionSerializer(serializers.ModelSerializer):

    answers = serializers.SerializerMethodField()
    question_type = serializers.SerializerMethodField()

    def get_answers(self, obj):
        return [
            {
                'id': answer.id,
                'answer': answer.answer,
                # 'is_correct': answer.is_correct
            } for answer in obj.answers.all()]

    def get_question_type(self, obj):
        return obj.question_type.name

    class Meta:
        model = Question
        fields = [
            'question_type',
            'attempts',
            'question',
            'answers',
        ]


class QuizSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        return obj.category.id

    def get_questions(self, obj):
        return [
            {'question_id': question.id,
             'question': question.question,
             'question_type': question.question_type.name,
             'question_status': question.status,
             #  'attempts': question.attempts,
             'answers':
             [
                 {
                     'answer_id': answer.id,
                     'answer': answer.answer,
                     'is_correct': answer.is_correct
                 } for answer in question.answers.all()]} for question in obj.questions.all()
        ]

    class Meta:
        model = Quiz
        fields = [
            'id',
            'name',
            'category',
            'questions',
        ]


class BotUsersSerializer(serializers.ModelSerializer):

    class Meta:
        model = BotUsers
        fields = [
            'id',
            'first_name',
            'phone_number',
            'category_id',
            'verification_code',
            'is_verified'
        ]


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = [
            'id',
            'answer',
            'is_correct',
        ]


class TempUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TempUser
        fields = [
            'id',
            'name',
            'phone_number',
        ]


class UserAnswersSerializer(serializers.ModelSerializer):

    is_correct = serializers.SerializerMethodField()

    def get_is_correct(self, obj):
        return obj.answer_id.is_correct

    class Meta:
        model = UserAnswers
        fields = [
            'id',
            'user_id',
            'question_id',
            'answer_id',
            'is_correct',
            # 'is_correct',
        ]


# class UserDetailSerializer(serializers.ModelSerializer):

#     user_id = serializers.SerializerMethodField()
#     questions = serializers.SerializerMethodField()
#     category_id = serializers.SerializerMethodField()
#     user_id_var = None
#     category_id_var = None

#     def get_category_id(self, obj):
#         self.category_id_var = obj.category_id.id
#         return obj.category_id.id

#     def get_user_id(self, obj):
#         global user_id_var
#         user_id_var = obj.user_id.id
#         print(user_id_var)
#         return obj.user_id.id

#     def get_questions(self, obj):
#         global user_id_var
#         data = [
#             {
#                 'question_id': question.id,
#                 'question_status': question.status,
#                 #  'attempts': question.attempts,
#                 'selected_answer': UserAnswers.objects.get(
#                     Q(user_id=user_id_var) & Q(question_id=question.id)).answer_id.id,
#                 'correct_answer':
#                 [
#                     {
#                         'answer_id': answer.id,
#                         'answer': answer.answer,
#                         # 'is_correct': answer.is_correct
#                     } for answer in question.answers.all()
#                     if answer.is_correct
#                 ]
#             } for question in obj.questions.all()
#         ]

#         for i in data:
#             # print(i['selected_answer'])
#             # print(i['correct_answer'][0]['answer_id'])
#             if i['selected_answer'] == i['correct_answer'][0]['answer_id']:
#                 i['question_status'] = 'correct'
#             else:
#                 i['question_status'] = 'incorrect'
#         return data

#     class Meta:
#         model = UserDetail
#         fields = [
#             'id',
#             'user_id',
#             'category_id',
#             'questions',
#         ]


class GetUserDetailSerializer(serializers.Serializer):

    id = serializers.IntegerField()
    category_id = serializers.SerializerMethodField()
    # required_questions = requests.get(

    def get_category_id(self, obj):
        return obj.category_id.id

    def get_questions(self, obj):
        data = [

        ]

    class Meta:
        model = GetUser
        fields = [
            'id',
            'category_id',
            'questions',
        ]
