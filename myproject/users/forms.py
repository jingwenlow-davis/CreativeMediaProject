# users/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser, Post


# class CustomAuthenticationForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super(MyLoginForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget.placeholder = 'Username'
#         self.fields['password'].widget.placeholder = 'Password'

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class AddPost(forms.Form):
    post = forms.CharField()
