from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import FileResponse, HttpResponse
from django.contrib import auth,messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from .forms import UserLoginForm, RegistrationForm
# Create your views here.

def home(request):
    user = request.user if request.user.is_authenticated else None
    context = {
        'user': user 
    }
    return render(request, "index.html", context)

def registration(request):
    """
    Handle Registration
    """
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form = form.save()
            return redirect('home')
       
    else:
        form = RegistrationForm()

    context={
        'form':form
    }
    return render(request,'registration.html',context)

@csrf_protect
def login(request):
    if request.user.is_authenticated:
        return redirect('/') 

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:  
                auth.login(request, user)
                return redirect('/')  # Redirect to the home page or another URL after successful login   
            else:
                form.add_error(None, "Error occurred")  # Add error to non-field error

    else:
        form = UserLoginForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)

def logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out")
    return redirect('home')