from django.db import models
import smtplib
import bcrypt
import re


class PostManager(models.Manager):
    def postValidation(self, postData):
        errors= {}
        if len(postData) > 0:

            return errors

class RegisterManager(models.Manager):
    def regValidation(self, postData):
        errors= {}
        if len(postData) > 0:
            userName= postData['user_name']
            userEmail= postData['user_email']
            userPass= postData['user_pass']
            passConfirm= postData['user_confirm']
            firstName= postData['user_first']
            lastName= postData['user_last']
            EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

            if len(userName) > 0:
                if len(User.objects.filter(user_name= userName)) > 0:
                    print('user name is taken. . .')
                    errors['USER_NAME_EXISTS_ERROR']= 'User name is taken.'
                if len(userName) < 5:
                    print('user name is less than 5 charaters. . .')
                    errors['USER_NAME_LEN_ERROR']= 'User name must be atleast 5 characters.'
            if len(userEmail) > 0:
                if len(User.objects.filter(user_email= userEmail)) > 0:
                    print('email is already in use')
                    errors['USER_EMAIL_EXISTS_ERROR']= 'Invalid email.'
                if not EMAIL_REGEX.match(userEmail):
                    errors['USER_EMAIL_FORMAT_ERROR']= 'Invalid email.'
            return errors
    def loginValidation(self, postData):
        errors= {}
        if len(postData) > 0:
            return errors

class Post(models.Model):
    post= models.CharField(max_length= 255)
    posted_by= models.ForeignKey(User, related_name='post', on_deleted= models.CASCADE)

    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)
    objects= PostManager()

class User(models.Model):
    first_name= models.CharField(max_length= 16)
    last_name= models.CharField(max_length= 16)
    user_name= models.CharField(max_length= 32)
    user_email= models.CharField(max_length= 32)
    password= models.CharField(max_length= 256)

    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)

    objects= RegisterManager()