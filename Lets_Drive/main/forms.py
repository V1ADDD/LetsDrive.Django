from django.forms import ModelForm, TextInput, PasswordInput, FileInput
from .models import Users, Breaks


class UsersForm(ModelForm):
    class Meta:
        model = Users
        fields = ['fio', 'password', 'photo_pass', 'photo_vu']
        widgets = {
            "fio": TextInput(attrs={
                'id': "fio",
                'onblur': "check()",
                'class': "form-control",
                'required': True
            }),
            "password": PasswordInput(attrs={
                'id': "password",
                'onblur': "check()",
                'class': "form-control",
                'required': True
            }),
            "photo_pass": FileInput(attrs={
                'id': "photo_pass",
                'accept': "image/*,image/jpeg",
                'class': "form-control",
                'required': True
            }),
            "photo_vu": FileInput(attrs={
                'id': "photo_vu",
                'accept': "image/*,image/jpeg",
                'class': "form-control",
                'required': True
            }),
        }
