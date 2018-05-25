from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser, Post
from django.forms import ModelForm

# login form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password'}))

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


# signup form
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='username',widget=forms.TextInput(attrs={'placeholder':'username'}))
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'password'}))
    password2 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'placeholder':'confirm password'}))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'password1', 'password2',)

# change user form: not used
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

# form to add post
class AddPost(ModelForm):
    post = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "100", 'rows': "20", }))
    img = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['post', 'img',]
