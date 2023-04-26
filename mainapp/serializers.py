from rest_framework import serializers
from .models import *


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
                     # 'is_correct': answer.is_correct
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

    class Meta:
        model = UserAnswers
        fields = [
            'id',
            'user_id',
            'question_id',
            'answer_id',
            # 'is_correct',
        ]


class UserDetailSerializer(serializers.ModelSerializer):

    questions = serializers.SerializerMethodField()

    def get_questions(self, obj):
        return [
            {'question_id': question.id,
             'question': question.question,
             'question_type': question.question_type.name,
             'question_status': question.status,
             #  'attempts': question.attempts,
             'answer': None,
             #  [
             #      {
             #          'answer_id': answer.id,
             #          'answer': answer.answer,
             #          # 'is_correct': answer.is_correct
             #      } for answer in question.answers.all()]
             } for question in obj.questions.all()
        ]

    class Meta:
        model = UserDetail
        fields = [
            'id',
            'user_id',
            'category_id',
            'questions',
        ]
