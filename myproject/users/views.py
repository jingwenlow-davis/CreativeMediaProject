from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views import generic
from django.views.generic import TemplateView
from django.core.exceptions import ValidationError

from .forms import CustomAuthenticationForm, CustomUserCreationForm, AddPost, AddFriend
from .models import Post, Friend, CustomUser
from .serializers import FriendSerializer, UserSerializer

from rest_framework import viewsets



# when user clicks login
def loginView(request):
    # why didn't this work?:
    # form = CustomAuthenticationForm(request.POST)
    # if request.method == "POST" and form.is_valid():
    #     username = form.cleaned_data['username']
    #     password = form.cleaned_data['password']
    username = request.POST.get('username') # get username
    password = request.POST.get('password') # get password
    user = authenticate(request, username=username, password=password) # authenticate user

    if user is not None and user.is_active:
        login(request, user) # log user in
        return HttpResponseRedirect('/home') # bring user to home page
    else:
        # stay on the same page for incorrect login
        return HttpResponseRedirect('/users/login')



# when user clicks signup
def signupView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username'] # get username
            password1 = form.cleaned_data['password1'] # get password
            password2 = form.cleaned_data['password2'] # get password
            if not password2: # make sure there is a second password
                raise forms.ValidationError("You must confirm your password")
                # print(form.errors)
            if password1 != password2: # make sure first and seocond passwords match!
                raise forms.ValidationError("Your passwords do not match")
                # print(form.errors)
            user = authenticate(request, username=username, password=password1) # authenticate user
            login(request, user) # login user
            return redirect('/home') # bring user to home page
        else:
            print(form.errors)
        #form = CustomUserCreationForm()
    return HttpResponseRedirect('/users/login')


# login view
class auth_login(TemplateView):
    template_name = 'login.html'
    def get(self, request):
        formA = CustomAuthenticationForm() # form to login
        formB = CustomUserCreationForm() # form to signup

        args = {'formA': formA, 'formB': formB}
        return render(request, self.template_name, args)



# home page view
class Home(TemplateView):
    template_name = 'home.html'
    def get(self, request):
        if request.user.is_authenticated:
            form = AddPost()
            if Friend.objects.filter(current_user=request.user): # check if user has friends
                friend = Friend.objects.filter(current_user=request.user) # get current user's friend object
                friends = friend[0].users.all() # get list of friends
                friends_ids = list(friends.values_list('id', flat=True)) # get list of ids of friends
                # filter only current user and their friend's posts
                posts = Post.objects.filter(user__id__in=friends_ids) | Post.objects.filter(user=request.user)
            else:
                posts = Post.objects.filter(user=request.user) # filter only user's own posts
            # list of all possible users not including current user
            users = CustomUser.objects.exclude(id=request.user.id)

            args = {'form': form, 'posts': posts, 'users':users}
            return render(request, self.template_name, args)
        else: # don't show posts if user is not authenticated
            return render(request, self.template_name)


# add post view
class addPost(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addPost.html'

    @method_decorator(login_required) # redirect to home if logged out
    def get(self, request):
        form = AddPost()
        friends = []
        posts = Post.objects.all() # get all posts
        users = CustomUser.objects.exclude(id=request.user.id) # get all users except current user
        if Friend.objects.filter(current_user=request.user):
            friend = Friend.objects.filter(current_user=request.user) # get current user's friend object
            friends = friend[0].users.all() # get all of current user's friends

        args = {'form': form, 'posts': posts, 'users':users, 'friends':friends}
        return render(request, self.template_name, args)

    def post(self, request):
        form = AddPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False) # save text and optional image
            post.user = request.user # save the user that posted it
            post.save() # save to database

            form = addPost()
            return redirect('addPost') # refresh addPost
        args = {'form': form}
        return render(request, self.template_name, args)


# add or remove friend view
class addFriend(TemplateView):
    success_url = reverse_lazy('login')
    template_name = 'addFriend.html'

    @method_decorator(login_required) # redirect to home if logged out
    def get(self, request):
        form = AddFriend()
        friends = []
        # get all users excluding current user
        users = CustomUser.objects.exclude(id=request.user.id)
        # check if user has friends
        if Friend.objects.filter(current_user=request.user):
            friend = Friend.objects.get(current_user=request.user) # get current users friends object
            friends = friend.users.all() # get current users friends

        args = {'users':users, 'friends':friends, 'form':form}
        return render(request, self.template_name, args)

# <QueryDict: {'csrfmiddlewaretoken': ['dxNvRZdleebpOYzhMIpZ9e7LjAk7mMdDLODjijZGe9PSzCa128qaiZiyhADHKT9K'], 'users': ['jingwenlow', 'sarah']}>

    def post(self, request):
        resp = request.POST.getlist('users') # get users to add to friends
        print(resp)

        for i in range(len(resp)):
            friend = CustomUser.objects.get(username=resp[i]) # get friend to add/remove
            Friend.make_friend(request.user, friend)

        friends = [] # list of current friends
        # get all users excluding current user
        users = CustomUser.objects.exclude(id=request.user.id)
        # check if user has friends
        if Friend.objects.filter(current_user=request.user):
            friend = Friend.objects.get(current_user=request.user) # get current users friends object
            friends = friend.users.all() # get current users friends

        form = AddFriend()
        args = {'users':users, 'friends':friends, 'form':form}
        return render(request, self.template_name, args)



# add or remove a friend
def change_friends(request, operation, pk):
    friend = CustomUser.objects.get(pk=pk) # get friend to add/remove
    if operation == 'add': # add friend
        Friend.make_friend(request.user, friend)

    elif operation == 'remove': # remove friend
        Friend.lose_friend(request.user, friend)

    return redirect('addFriend') # refresh page


@csrf_exempt
def friend_list(request, username):

    if request.method == 'GET':
        current_user = CustomUser.objects.get(username=username)
        friend = Friend.objects.filter(current_user=current_user) # get current user's friend object
        friends = friend[0].users.all() # get all of current user's friends
        serializer = UserSerializer(friends, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view users.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class FriendViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view friends.
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
