from django.shortcuts import render, redirect
from users.forms import UserCreationForm, UserLoginForm
from django.contrib.auth import login as LOGIN
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import request
from users.models import CustomUser

#from .forms import CustomUserCreationForm
#from .models import UserProfile
#from .backends import CustomUserAuth as auth
# Create your views here.

def index(request):
    return render(request, 'users/index.html')

def login(request):
    form = UserLoginForm(request.POST or None)
    next_url = request.GET.get('next')
    if request.method == 'POST':
        if form.is_valid():
            user_obj = form.cleaned_data.get('user_obj')
            LOGIN(request, user_obj)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('home-view')
        else:
            messages.warning(request, f'Invalid Credentials')
    
    return render(request, 'users/login.html', {"form": form})

def register(request):
    form = UserCreationForm(request.POST or None)
    context = {
            'form': form
	    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('login-view')
        else:
            return redirect('login-view')
    else:
        return render(request, 'users/register.html', context)

def scout(request):
    return render(request, 'users/scout.html')

def scouthub(request):
    return render(request, 'users/scouthub.html')

@login_required
def profile(request):
    return render(request, 'users/profile.html')