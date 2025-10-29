from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CustomUserCreationForm



# Create your views here.
class Login(LoginView):
    template_name = 'login.html'

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():

            user = form.save()
            login(request, user)
            return redirect('home')
        else: 
            error_message = "Invalid sign up - try again"
    
    form = CustomUserCreationForm()
    context = {'form': form, 'error_message' : error_message}
    return render(request, 'signup.html', context)

def account(request):
    return render(request, "account.html")

def home(request):
    return render(request, "home.html")

def about(request):
    return render(request,"about.html")


