from django.contrib import admin
from .models import *


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'date_created', 'date_updated')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'is_correct', 'date_created')


@admin.register(BotUsers)
class BotUsersAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'id', 'phone_number'
    )


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(QuestionType)
class QuestionTypeAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'date_created']


@admin.register(TempUser)
class TempUserAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'phone_number']
