from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from .forms import CustomRegistrationForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash


def register(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')

    return render(request, 'auth/auth.html', {'form': form,'page': 'register'})


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ChangePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                login(request, request.user)
                messages.success(request, 'Your password has been changed successfully.')
                return redirect('home') 
            else:
                for error in list(form.errors.values()):
                    messages.error(request, ', '.join([str(e) for e in error]))
        else:
            form = ChangePasswordForm(user=request.user)
        return render(request, 'custom_auth/change_password.html', {'form': form})
    messages.error(request, 'You need to be logged in to change your password.')
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'auth/login.html', {'page': 'login'})



def logout_view(request):
    logout(request)
    return redirect('login')


def update_user(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            full_name = request.POST.get('full_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            user = request.user
            user.full_name = full_name
            user.username = username
            user.email = email
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('home') 
        return render(request, 'custom_auth/update_user.html', {'user': request.user})
    messages.error(request, 'You need to be logged in to update your profile.')
    return redirect('login')