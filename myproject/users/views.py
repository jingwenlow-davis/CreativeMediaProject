from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
# users/views.py
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView

# from django.views.generic.edit  import CreateView

from django.http import HttpResponse
from .forms import CustomAuthenticationForm, CustomUserCreationForm, AddPost
from .models import Post, Friend, CustomUser


# class SignUp(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'signup.html'


# class LoginView(generic.FormView):
#     form_class = LoginForm
#     success_url = reverse_lazy('home')
#     template_name = 'registration/login.html'
#
#     def form_valid(self, form):
#      username = form.cleaned_data['username']
#      password = form.cleaned_data['password']
#      user = authenticate(username=username, password=password)
#
#      if user is not None and user.is_active:
#          login(self.request, user)
#          return super(LoginView, self).form_valid(form)
#      else:
#          return self.form_invalid(form)

def loginView(request):
    form = CustomAuthenticationForm(request.POST)
    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return HttpResponseRedirect('/home')
         # return render('home.html', args)
         # return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)
    return HttpResponseRedirect('/home')




def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            raw_password = form.cleaned_data['password1']
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = CustomUserCreationForm()
    return HttpResponseRedirect('/home')
    # return render(request, 'signup.html', {'form': form})



class newLogin(TemplateView):
    template_name = 'newLogin.html'
    def get(self, request):
        formA = CustomAuthenticationForm()
        formB = CustomUserCreationForm()

        args = {'formA': formA, 'formB': formB}
        return render(request, self.template_name, args)




class Home(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        if request.user.is_authenticated:
            form = AddPost()
            friend = Friend.objects.filter(current_user=request.user) # get current user's friend object
            friends = friend[0].users.all() # get list of friends
            friends_ids = list(friends.values_list('id', flat=True)) # get list of ids of friends
            # filter only current user and their friend's posts
            posts = Post.objects.filter(user__id__in=friends_ids) | Post.objects.filter(user=request.user)
            # list of all possible users not including current user
            users = CustomUser.objects.exclude(id=request.user.id)

            args = {'form': form, 'posts': posts, 'users':users}
            return render(request, self.template_name, args)
        else:
            return render(request, self.template_name)


class addPost(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addPost.html'

    @method_decorator(login_required) # redirect to home if logged out
    def get(self, request):
        form = AddPost()
        posts = Post.objects.all() # get all posts
        users = CustomUser.objects.exclude(id=request.user.id) # get all users except current user
        friend = Friend.objects.filter(current_user=request.user) # get current user's friend object
        friends = friend[0].users.all() # get all of current user's friends

        args = {'form': form, 'posts': posts, 'users':users, 'friends':friends}
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            # instance = AddPost(img=request.FILES['file'])
            # instance.save()
            post.user = request.user
            post.save()

            # text = form.cleaned_data['post']
            form = addPost()
            return redirect('addPost')
        args = {'form': form}
        return render(request, self.template_name, args)


class addFriend(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addFriend.html'

    @method_decorator(login_required) # redirect to home if logged out
    def get(self, request):
        users = CustomUser.objects.exclude(id=request.user.id) #
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
