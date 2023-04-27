from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class TempUser(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id) + ' ' + self.name


class Category(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class BotUsers(models.Model):
    id = models.CharField(("id"), max_length=100,
                          primary_key=True, unique=True)

    # ? очки за игру
    # ? points = models.IntegerField(default=0)

    first_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    category_id = models.ForeignKey(
        "mainapp.Category", verbose_name=("category_id"), on_delete=models.CASCADE, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'BotUser'
        verbose_name_plural = 'BotUsers'


class QuestionType(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Answer(models.Model):
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.answer


class Question(models.Model):
    CHOICES = (
        ('correct', 'correct'),
        ('incorrect', 'incorrect'),
        ('wait', 'wait'),
    )
    question_type = models.ForeignKey(
        'mainapp.QuestionType', on_delete=models.CASCADE, related_name='Type', default=1)
    attempts = models.IntegerField(default=3)
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField(
        'mainapp.Answer', related_name='Question', blank=True)
    status = models.CharField(
        ('status'), max_length=100, choices=CHOICES, default='wait')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['-date_created']

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Question'


class Quiz(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        'mainapp.Category', on_delete=models.CASCADE, related_name='Category')
    questions = models.ManyToManyField('mainapp.Question', related_name='Quiz')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Quiz'
        verbose_name_plural = 'Quiz'


class UserAnswers(models.Model):
    user_id = models.ForeignKey(
        'mainapp.BotUsers', on_delete=models.CASCADE, related_name='User')
    question_id = models.ForeignKey(
        'mainapp.Question', on_delete=models.CASCADE, related_name='Question')
    answer_id = models.ForeignKey('mainapp.Answer', on_delete=models.CASCADE)


# class UserDetail(models.Model):
#     # id = models.ForeignKey(
#     #     'mainapp.BotUsers', on_delete=models.CASCADE, primary_key=True, unique=True)
#     user_id = models.ForeignKey('mainapp.BotUsers', on_delete=models.CASCADE)
#     category_id = models.ForeignKey(
#         'mainapp.Category', on_delete=models.CASCADE)
#     # selected_answer = models.ForeignKey(
#     #     'mainapp.Answer', on_delete=models.CASCADE, default=1)
#     # selected_answer = models.CharField(max_length=255, default='1')
#     questions = models.ManyToManyField(
#         'mainapp.Question')


class GetUser(models.Model):
    id = models.CharField(("user_id"), max_length=100, primary_key=True)
    category_id = models.ForeignKey(
        'mainapp.Category', on_delete=models.CASCADE, blank=True, null=True)
    selected_answer = models.ForeignKey(
        'mainapp.Answer', on_delete=models.CASCADE, default=None)
    questions = models.ManyToManyField('mainapp.Question')
