from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

# login should be the landing page of localhost:8000/
# The following URLS are for RENDER
def index(request):
    return render(request, 'login.html')

def dashboard(request):
    if 'uuid' not in request.session:
        print("No session in progress, you failed the vibe check.")
        return redirect('/')
    
    this_user = User.objects.get(id=request.session['uuid'])
    every_users_post = Post.objects.all()
    this_users_post = this_user.post.all()
    
    print("You are in the dashboard! Let's start listening!")
    context = {
        'user_object' : this_user,
        'every_users_post' : every_users_post,
    }
    
    return render(request,'dashboard.html', context)

#########################################################

#This is the end of the URLS for RENDER
def register(request):
    print("Register function", request.POST)
    errors = User.objects.

#The following URLS are for REDIRECTING









# This is the end of the URLS for REDIRECTING