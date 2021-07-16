from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login,logout
from django.contrib.auth.models import User, auth

# Create your views here.
def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        email = request.POST['email']

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password1, email=email)
        user.save()
        print(user)
        # user1 = auth.authenticate(username=username, password=password1)
        # form = UserCreationForm(request.POST)
        # print(form, request.POST)
        # if form.is_valid():
        #     user = form.save()
        #     print(user)
        login(request,user)
        return redirect('/')
    else:
        print("fail")
        # form = UserCreationForm()
    return redirect('/')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username1']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            print('Login Failed 1')
        # form = AuthenticationForm(data=request.POST)
        # print(form, request.POST)
        # if form.is_valid():
        #     user = form.get_user()
        #     print(user)
    else:
        print('Login Failed 2')
        # form = AuthenticationForm()
    return redirect('/')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('/')