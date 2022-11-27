from django import forms
from django.forms import widgets
from .models import Comment, Post, Profile, Message



class ProfileForm (forms.ModelForm):
  class Meta:
    model = Profile
    exclude = ['owner']
    widgets = {
        'name': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Full name'}),
        'username': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'username','disabled':True}),
        'email': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
        'about_me': widgets.Textarea(attrs={'class': 'form-control','placeholder':'About yourself'}),
        'profile_picture': widgets.FileInput(attrs={'class': 'custom-file-input'}),
        'cover_picture': widgets.FileInput(attrs={'class': 'custom-file-input'}),
        'intro': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Intro'}),
        'occupation': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Occupation'}),
        'country': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Country'}),
        'mobile': widgets.TextInput(attrs={'class': 'form-control', 'placeholder':'Mobile Phone'}),
        'facebook_link': widgets.URLInput(attrs={'class': 'form-control'}),
        'youtube_link': widgets.URLInput(attrs={'class': 'form-control'}),
        'instagram_link': widgets.URLInput(attrs={'class': 'form-control'}),
        'twitter_link': widgets.URLInput(attrs={'class': 'form-control'}),
        'website_link': widgets.URLInput(attrs={'class': 'form-control'}),
    }


class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    exclude = ['likes']
    widgets = {
      'owner': widgets.HiddenInput(),
      'body': widgets.Textarea(attrs={'class': 'form-control h-100'}),
      'title': widgets.TextInput(attrs={'class': 'form-control my-3',"placeholder": "Post title"}),
      'image': widgets.ClearableFileInput(attrs={'class': 'custom-file-input'}),
    }


  
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['body']
    widgets = {
      'body': widgets.Textarea(attrs={'name':'comment','class':'form-control','rows':5})
    }

class MessageForm(forms.ModelForm):
  class Meta:
    model = Message
    fields = ['message']
    widgets = {
        'message': widgets.Textarea(attrs={'class': 'form-control', 'placeholder':'Write your message','rows':5,}),
    }


