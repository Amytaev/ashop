from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from .models import CustomUser
from .models import Post
import re

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['avatar']

class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Повторите пароль', required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже занят.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError("Этот никнейм уже занят.")
        return username

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("Этот номер телефона уже занят.")
        if not re.match(r'^\+?[0-9]{10,15}$', phone):  # Проверка формата телефона
            raise ValidationError("Введите корректный номер телефона.")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8:
            raise ValidationError("Пароль должен содержать хотя бы 8 символов.")
        if not re.search(r'[0-9]', password):  # Проверка на цифры
            raise ValidationError("Пароль должен содержать хотя бы одну цифру.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Пароли не совпадают.")

    def save(self, commit=True):
        user = super().save(commit=False)  # Создаем пользователя, но еще не сохраняем его в базе данных
        password = self.cleaned_data["password"]
        user.set_password(password)  # Хешируем пароль
        if commit:
            user.save()  # Сохраняем пользователя в базе данных
        return user

class LoginForm(forms.Form):
    identifier = forms.CharField(
        label='Email или никнейм',
        max_length=254,
        initial='',  # Пустая строка по умолчанию
    )
    password = forms.CharField(widget=forms.PasswordInput)

def clean(self):
    cleaned_data = super().clean()
    identifier = cleaned_data.get('identifier', '').strip()
    password = cleaned_data.get('password')

    if identifier and password:
        # Если это email, ищем пользователя по email
        if '@' in identifier:
            user = authenticate(request=self.request, email=identifier, password=password)
        else:
            # Если это username, ищем по username
            user = authenticate(request=self.request, username=identifier, password=password)

        if user is None:
            raise forms.ValidationError("Неверные данные для входа.")

        # Дополнительные проверки на статус пользователя
        if not user.is_active:
            raise forms.ValidationError

        if not user.is_staff:
            raise forms.ValidationError

    return cleaned_data




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']  # Добавлено поле title

