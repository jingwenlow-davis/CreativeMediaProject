from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# Create your views here.
# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
# from django.views.generic.edit  import CreateView

from django.http import HttpResponse
from .forms import CustomUserCreationForm, AddPost
from .models import Post, Friend, CustomUser

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# def addPost(request):
#     return render(request, 'addPost.html', addPost)
#

class Home(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        form = AddPost()
        posts = Post.objects.all()
        users = CustomUser.objects.exclude(id=request.user.id)

        args = {'form': form, 'posts': posts, 'users':users}
        return render(request, self.template_name, args)



class addPost(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addPost.html'

    def get(self, request):
        form = AddPost()
        posts = Post.objects.all()
        users = CustomUser.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()

        args = {'form': form, 'posts': posts, 'users':users, 'friends':friends}
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            text = form.cleaned_data['post']
            form = addPost()
            return redirect('addPost')
        args = {'form': form, 'text': text}
        return render(request, self.template_name, args)


def change_friends(request, operation, pk):
    friend = User.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)

    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)
    return redirect('home.html')


class addFriend(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addFriend.html'


# class JointLoginSignupView(CreateView):
#     form_class = CustomAuthenticationForm
#     signup_form  = CustomUserCreationForm
#     template_name = 'login.html'
#     def __init__(self, **kwargs):
#         super(JointLoginSignupView, self).__init__(*kwargs)
#
#     def get_context_data(self, **kwargs):
#         ret = super(JointLoginSignupView, self).get_context_data(**kwargs)
#         ret['signupform'] = get_form_class(app_settings.FORMS, 'CustomUserCreationForm', self.signup_form)
#         return ret
#
#
# login = JointLoginSignupView.as_view()
