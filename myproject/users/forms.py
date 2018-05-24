from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from .models import CustomUser, Post
from django.forms import ModelForm

# login form
class CustomAuthenticationForm(AuthenticationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


# signup form
class CustomUserCreationForm(UserCreationForm):

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
    post = forms.CharField(widget=forms.Textarea(attrs={'width':"100%", 'cols' : "95", 'rows': "20", }))
    img = forms.FileField(required=False)

    class Meta:
        model = Post
        fields = ['post', 'img',]
