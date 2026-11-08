import os
from django import forms
from django.core.validators import RegexValidator
from .models import User, Application


class RegisterForm(forms.ModelForm):
    fio = forms.CharField(
        label='ФИО', max_length=150,
        validators=[RegexValidator(r'^[А-Яа-яЁё\s-]+$',
                    'ФИО: только кириллические буквы, дефис и пробелы.')],
    )
    username = forms.CharField(
        label='Логин', max_length=150,
        validators=[RegexValidator(r'^[A-Za-z-]+$',
                    'Логин: только латинские буквы и дефис.')],
    )
    email = forms.EmailField(label='Email')   # проверка email встроена
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput)
    consent = forms.BooleanField(
        label='Согласие на обработку персональных данных',
        error_messages={'required': 'Необходимо дать согласие на обработку персональных данных.'},
    )

    class Meta:
        model = User
        fields = ['fio', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name != 'consent':
                field.widget.attrs['class'] = 'form-control'
            else:
                field.widget.attrs['class'] = 'form-check-input'

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            self.add_error('password2', 'Пароли не совпадают.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.consent = True
        if commit:
            user.save()
        return user

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['title', 'description', 'category', 'image']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'category': 'Категория',
            'image': 'Фото помещения или план',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'image':
                field.widget.attrs['class'] = 'form-control-file'
            else:
                field.widget.attrs['class'] = 'form-control'
        self.fields['category'].empty_label = 'Выберите категорию'

    # проверка файла: формат и размер
    def clean_image(self):
        image = self.cleaned_data['image']
        ext = os.path.splitext(image.name)[1].lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.bmp']:
            raise forms.ValidationError('Допустимые форматы: jpg, jpeg, png, bmp.')
        if image.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Размер файла не должен превышать 2 Мб.')
        return image