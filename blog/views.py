from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags

# Home


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts, 'home': 'active'})


# About
def about(request):
    return render(request, 'blog/about.html', {'about': 'active'})


# Contact
def contact(request):
    return render(request, 'blog/contact.html', {'contact': 'active'})


# Dashboard
"""def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        grps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'dashboard': 'active', 'posts': posts, 'full_name': full_name, 'groups': grps})
    else:
        return HttpResponseRedirect('/login/')"""


@login_required
def dashboard(request):
    posts = Post.objects.all()
    user = request.user
    full_name = user.get_full_name()
    grps = user.groups.all()
    return render(request, 'blog/dashboard.html', {'dashboard': 'active', 'posts': posts, 'full_name': full_name, 'groups': grps})


# Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


# Signup
def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(
                request, "Congratulations! You've become an author.")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)

    else:
        form = SignUpForm()
    return render(request, 'blog/signup.html', {'form': form, 'signup': 'active'})


# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged In Successfully !!")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form, 'login': 'active'})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add Posts


@login_required
def add_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                description = form.cleaned_data['description']
                add = Post(title=title, description=description)
                add.save()
                messages.success(request, "Post Added Successfully !!")
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Update Posts


@login_required
def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, "Post Updated Successfully !!")
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, 'blog/editpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')

# Delete Posts


@login_required
def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request, "Post Deleted Successfully !!")
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
