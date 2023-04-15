from django.shortcuts import render,redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required

def mypg(request):
    user = User.objects.get(username=request.user.username)
    context = {
        'user':user
    }
    return render(request, 'accounts/mypg.html', context)

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')
    if request.method=="POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('reviews:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('accounts:login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('reviews:index')
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('reviews:index')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)

@login_required
def delete(request):
    request.user.delete()
    auth_logout(request)
    return redirect('reviews:index')

@login_required
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('reviews:index')
    else:
        form = CustomUserChangeForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)

@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('reviews:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)