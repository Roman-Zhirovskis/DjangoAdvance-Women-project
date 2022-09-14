from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.views import AuthenticationForm
from captcha.fields import CaptchaField

from .models import *


# class AddPostForm(forms.Form):
#     title = forms.CharField(max_length=255, label='Заголовок')
#     slug = forms.SlugField(max_length=255)
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
#     is_published = forms.BooleanField()
#     cat = forms.ModelChoiceField(queryset=Category.objects.all())


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Not selected cat"

    class Meta:
        model = Women
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        widget = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-input'}, )
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Len title more than 200 simv')

        return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AuthenticationUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    # email = forms.EmailField(label='Email', max_length=255)
    subject = forms.CharField(label='Тема', max_length=255, widget=forms.TextInput(attrs={'class': 'form-input'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-input'}))
    captcha = CaptchaField()
