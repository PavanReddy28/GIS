from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User, auth
from django.contrib import messages


def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        email = request.POST['email']
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, '"'+username+'" already exists. Please try again with a different username.')
            if User.objects.filter(email=email).exists():
                messages.add_message(request, messages.ERROR, 'There is already an account with username "'+str(User.objects.filter(email=email)[0])+'" registered on the mentioned email. Please login.')
                return redirect('/')
            return redirect('/')
        elif User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'There is already an account with username "'+str(User.objects.filter(email=email)[0])+'" registered on the mentioned email. Please login.')
            return redirect('/')
        else:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password1, email=email)
            user.save()
            login(request,user)
            messages.add_message(request, messages.SUCCESS, 'Welcome aboard '+first_name+'! You are registered on GIS-World.')
            return redirect('/')
    else:
        print("fail")
    messages.add_message(request, messages.ERROR, 'Sign up Failed! Please try again.')
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username1']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Welcome back '+user.first_name+'! You are logged in.')
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, 'Login Falied! Username or Password is incorrect.')
            redirect('/')
    else:
        print('Login Failed 2')
    return redirect('/')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Thank You for using GIS-world! You have succesfully logged out.')
        return redirect('/')