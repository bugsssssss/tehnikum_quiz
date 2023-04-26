from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class TempUser(models.Model):
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)

    def __str__(self):
        return str(self.id) + ' ' + self.name


class BotUsers(models.Model):
    id = models.CharField(("id"), max_length=100,
                          primary_key=True, unique=True)

    # ? очки за игру
    # ? points = models.IntegerField(default=0)

    first_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    verification_code = models.CharField(max_length=255)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'BotUser'
        verbose_name_plural = 'BotUsers'


class Category(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


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
    question_type = models.ForeignKey(
        'mainapp.QuestionType', on_delete=models.CASCADE, related_name='Type', default=1)
    attempts = models.IntegerField(default=3)
    question = models.CharField(max_length=255)
    answers = models.ManyToManyField(
        'mainapp.Answer', related_name='Question', blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

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
