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

#This is the end of the URLS for RENDER

#########################################################

#The following URLS are for REDIRECTING

def register(request):
    print("Register function", request.POST)
    errors = User.objects.regValidation(request.POST)
    if len(request.POST) > 0:

        if len(errors) > 0:
            print("There are errors with the registration")
            for key, value in errors.items():
                messages.error(request,value)
                return redirect('/abc')
            
        else:
            print("Registration successful")
            #The following is to hash the password
            hash_slinging_slasher = bcrypt.hashpw(
                request.POST['user_pass'].encode(),
                bcrypt.gensalt()
            ).decode()
            # This is the end of the hash
            print(f"Our hash: {hash_slinging_slasher}")
            #Add user to database
            
            created_user = User.objects.create(
                first_name = request.POST['first_name'],
                last_name = request.POST['last_name'],
                user_name = request.POST['user_name'],
                user_email = request.POST['email'],
                password = hash_slinging_slasher
                # This will scramble the password and make it encrypted
            )
            print("Our newly registered user pass; ", created_user.password)
            print(f"My newly created user's id is {created_user.id}")
            # This will set us up in session
            request.session['uuid'] = created_user.id
            return redirect('/dashboard')
    return render(request, 'register.html')

# This will be for the logout
def logout(request):
    request.session.flush()
    return redirect('/')

# This will be for the login
def login(request):
    print(f"our post data is {request.POST}")
    # Check password through validator
    if len(request.POST) > 0:
        errors = User.objects.loginValidation(request.POST)
        if len(errors) > 0:
            print("There are errors in the login")
            for key, value in errors.item():
                messages.error(request, value)
            return redirect('/')
    
        else:
            # Check email in database
            # user_list = User.objects.filter(email=request.POST['user_email'])
            user_list= User.objects.get(user_email= request.POST['user_email'])
            # setup user in session
            request.session['uuid'] = user_list.id
            return redirect('/dashboard')
    else:
        return render(request, 'login.html')

# This is to be able to delete the post
def delete_post(request, post_text_id):
    this_post = Post.objects.get(id = post_text_id)
    this_post.delete()
    print(f'{this_post.id} ID Post was deleted successfully')
    return redirect('/dashboard')

# This is to be able to add posts
def add_post(request):
    errors = Post.objects.postValidation(request.POST)
    # Validate
    if len(errors) > 0:
        print("Something went wrong when adding this post")
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/dashboard')
    this_user = User.objects.get(id=request.session['uuid'])
    share_your_idea = Post.objects.create(
        post_text = request.POST['post_text'],
        artist_name= request.POST['artist_name'],
        song_name= request.POST['song_name'],
        album_pic= request.POST['album_pic'],
        posted_by = this_user,
    )
    return redirect('/dashboard')

# This is to be able to like posts
def likes(request, post_text_id):
    this_post = Post.objects.get(id=post_text_id)
    this_user = User.objects.get(id=request.session['uuid'])
    this_post.liked_by.add(this_user)
    
    return redirect(f'/dashboard/{this_post.id}')

# This is to display all the posts
def all_posts(request, post_text_id):
    context = {
        'this_post': Post.objects.get(id=post_text_id),
        'this_user' : User.objects.get(id = request.session['uuid']),
    }
    return render (request, 'dashboard.html', context)

# This is to be able to dislike
def dislike_post(request, post_text_id):
    this_post = Post.objects.get(id=post_text_id)
    this_user = User.objects.get(id=request.session['uuid'])
    this_post.liked_by.remove(this_user)
    return redirect(f'/dashboard/{post_text_id}')


# This is the end of the URLS for REDIRECTING
