from django import forms
from .models import *


class BotUsersForm(forms.ModelForm):

    class Meta:
        model = BotUsers
        fields = ['first_name', 'phone_number', 'verification_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'first_name'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'phone_number'}),
            'verification_code': forms.TextInput(attrs={'placeholder': 'verification_code'}),
        }

    # def clean(self):
    #     cleaned_data = super().clean()
    #     username = cleaned_data.get('username')
    #     first_name = cleaned_data.get('first_name')
    #     last_name = cleaned_data.get('last_name')
    #     if username == first_name == last_name:
    #         raise forms.ValidationError(
    #             'Username, first_name and last_name must be different')

    # def save(self, commit=True):
    #     instance = super().save(commit=False)
    #     instance.save()
    #     return instance

# class QuestionForm(forms.ModelForm):

#     class Meta:
#         model = Question
#         fields = '__all__'

#     def clean(self):
#         cleaned_data = super().clean()
#         question = cleaned_data.get('question')
#         answer = cleaned_data.get('answer')
#         if question == answer:
#             raise forms.ValidationError(
#                 'Question and answer must be different')

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.save()
#         return instance
