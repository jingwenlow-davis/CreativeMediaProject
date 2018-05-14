from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


class Home(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        if request.user.is_authenticated:
            form = AddPost()
            friend = Friend.objects.filter(current_user=request.user)
            friends = friend[0].users.all()
            friends_list = list(friends)
            posts = Post.objects.all() #filter(user__id_in=friends_list)
            users = CustomUser.objects.exclude(id=request.user.id)

            args = {'form': form, 'posts': posts, 'users':users}
            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name)


class addPost(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addPost.html'

    @method_decorator(login_required)
    def get(self, request):
        form = AddPost()
        posts = Post.objects.all()
        users = CustomUser.objects.exclude(id=request.user.id)
        friend = Friend.objects.filter(current_user=request.user)
        friends = friend[0].users.all()

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


class addFriend(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addFriend.html'

    @method_decorator(login_required)
    def get(self, request):
        users = CustomUser.objects.exclude(id=request.user.id)
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()

        args = {'users':users, 'friends':friends}
        return render(request, self.template_name, args)



def change_friends(request, operation, pk):
    friend = CustomUser.objects.get(pk=pk)
    if operation == 'add':
        Friend.make_friend(request.user, friend)

    elif operation == 'remove':
        Friend.lose_friend(request.user, friend)

    return redirect('addFriend')

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
