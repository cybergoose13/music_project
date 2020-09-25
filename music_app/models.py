from django.db import models
from email.message import EmailMessage
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import smtplib
import bcrypt
import re


class PostManager(models.Manager):
    def postValidation(self, postData):
        CLIENT_ID= 'f08fd973a07f4ba8849f5109c963b460'
        CLIENT_SECRET= '544cb114d54e47da8a6bedd7a412fb7f'
        auth_manager= SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp= spotipy.Spotify(auth_manager= auth_manager)
        
        artist= postData['artist_name'].title()
        song= postData['song_name'].title()
        result= sp.search(q=song, limit=20)

        songData = {}
        errors= {}

        if len(result['tracks']['items']) < 1:
            errors['QUERY_ERROR']= 'No song or artist was found.'
        else:
            for idx, track in enumerate(result['tracks']['items']):
                print(idx,track['name'],track['artists'][0]['name'], track['album']['images'][0]['url'])
                if track['artists'][0]['name'] == artist:
                    print('Match was found')
                    songData['album_image']= track['album']['images'][0]['url']
                    songData['artist_name']= artist
                    songData['song_name']= song

        return errors, songData

class RegisterManager(models.Manager):
    def regValidation(self, postData):
        errors= {}
        if len(postData) > 0:
            userName= postData['user_name']
            userEmail= postData['email']
            userPass= postData['user_pass']
            passConfirm= postData['confirm_pass']
            firstName= postData['first_name']
            lastName= postData['last_name']
            EMAIL_REGEX= re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
            PASS_REGEXT= ''

            
            if len(User.objects.filter(user_name= userName)) > 0:
                print('user name is taken. . .')
                errors['USER_NAME_EXISTS_ERROR']= 'User name is taken.'
            if len(userName) < 5:
                print('user name is less than 5 charaters. . .')
                errors['USER_NAME_LEN_ERROR']= 'User name must be atleast 5 characters.'
            if len(User.objects.filter(user_email= userEmail)) > 0:
                print('email is already in use. . .')
                errors['USER_EMAIL_EXISTS_ERROR']= 'Invalid email.'
            if not EMAIL_REGEX.match(userEmail):
                print('user email syntax error. . .')
                errors['USER_EMAIL_FORMAT_ERROR']= 'Invalid email.'
            
            if not re.match(r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$])[\w\d!@#$]{8,}$', userPass):
                print('password syntax error. . .')
                errors['PASSWORD_FORM_ERROR']= 'Password must have atleast 1 lowercase 1 uppercase and special character.'
            if userPass != passConfirm:
                print('passwords do not match error. . .')
                errors['PASSWORD_MATCH_ERROR']= 'Passwords do not match.'
            if len(firstName) < 5:
                print('first name is null or less than 5 char. . .')
                errors['FIRST_NAME_ERROR']= 'First name must have atleast 5 characters.'
            if len(lastName) < 5:
                print('last name is null or less than 5 char. . .')
                errors['LAST_NAME_ERROR']= 'Last name must have atleast 5 characters.'

        return errors

    def loginValidation(self, postData):
        errors= {}
        print(postData['user_pass'] + ' ' + postData['user_email'])
        
        if len(User.objects.filter(user_email= postData['user_email'])) == 0:
            print('email not found. . .')
            errors['LOGIN_ERROR']= 'Invalid login credentials.'
        else:
            if not bcrypt.checkpw(postData['user_pass'].encode(), User.objects.get(user_email= postData['user_email']).password.encode()):
                print('password did not match')
                errors['LOGIN_ERROR']= 'Invalid login credentials.'
        return errors

    def resetPassword(self, postData):
        user= User.objects.get(user_email= postData['user_email'])
        from_= 'cyberhack.inc@gmail.com'
        acc_pass= 'hzkbqnofoipuskgqk'
        to= user.user_email
        subject= 'Password Reset'
        body= 'Test'

        msg= EmailMessage()
        msg.set_content(body)
        msg['subject']= subject
        msg['to']= to
        msg['from']= from_

        server= smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_, acc_pass)
        server.send_message(msg)
        server.quit()

class Post(models.Model):
    post_text = models.CharField(max_length= 255)
    artist_name= models.CharField(max_length= 255)
    song_name= models.CharField(max_length= 255)
    album_pic= models.CharField(max_length= 255)
    posted_by = models.ForeignKey('User', related_name ='post', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = PostManager()

class User(models.Model):
    first_name= models.CharField(max_length= 16)
    last_name= models.CharField(max_length= 16)
    user_name= models.CharField(max_length= 32)
    user_email= models.CharField(max_length= 32)
    password= models.CharField(max_length= 256)

    created_at= models.DateTimeField(auto_now_add= True)
    updated_at= models.DateTimeField(auto_now= True)

    objects= RegisterManager()