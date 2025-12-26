from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Customer
from .forms import CustomerRegistrationForm, ChangePasswordForm
import json


def register(request):
    form = CustomerRegistrationForm()
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful. Please complete your profile.')
            return redirect('update_user')
        for error in list(form.errors.values()):
            messages.error(request, ', '.join([str(e) for e in error]))
    return render(request, 'custom_auth/register.html', {'form': form})


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
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid email or password. Please try again.')
    return render(request, 'custom_auth/login.html')


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