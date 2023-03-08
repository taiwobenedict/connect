from email.policy import default
from django.core.mail import send_mail
from Blog import settings
from django.db import models
from django.contrib.auth.models import User
# Calling uuid like this "uuid.uuid4()" will break the code. Just leave it like this "uuid.uuid4"
import uuid
from django.db.models.signals import post_save, pre_save
from PIL import Image
from .img import image_resize

# Create your models here.


class Post(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name='post')
    image = models.ImageField(blank=True, upload_to='Post_images/')
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    id = models.UUIDField(max_length=100, default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f'{self.owner}-post'

    def save(self, *args, **kwargs):
        if self.image:
            image_resize(self.image, 1080, 1080)
        super().save(*args, **kwargs)

    def ImageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

    def total_likes(self):
        total = self.likes.count()
        return total


class Comment(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    body = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(max_length=100, default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.body


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    name = models.CharField(max_length=30, null=True, blank=True)
    username = models.CharField(max_length=30, null=True, blank=True)
    intro = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.ImageField(
        blank=True, upload_to="Profile_images/")
    cover_picture = models.ImageField(
        blank=True, upload_to="cover_images/")
    occupation = models.CharField(max_length=50, null=True, blank=True)
    about_me = models.TextField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    website_link = models.URLField(max_length=200, null=True, blank=True)
    facebook_link = models.URLField(max_length=200, null=True, blank=True)
    twitter_link = models.URLField(max_length=200, null=True, blank=True)
    instagram_link = models.URLField(max_length=200, null=True, blank=True)
    youtube_link = models.URLField(max_length=200, null=True, blank=True)
    id = models.UUIDField(max_length=100, default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)

    def __str__(self):
        return f'{self.owner} profile'

    def save(self, *args, **kwargs):
        if self.profile_picture:
            image_resize(self.profile_picture,800,800)
        if self.cover_picture:
            image_resize(self.cover_picture,500,500)
        super().save(*args, **kwargs)

    def ProfileImageUrl(self):
        try:
            url = self.profile_picture.url
        except:
            url = 'https://mydjangoimage-bucket.s3.us-west-2.amazonaws.com/Default_images/kindpng_4517876.png'
        return url

    def CoverImageUrl(self):
        try:
            url = self.cover_picture.url
        except:
            url = 'https://mydjangoimage-bucket.s3.us-west-2.amazonaws.com/Default_images/kindpng_4517876.png'
        return url


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sender')
    reciever = models.ForeignKey(
        Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='reciever')
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(max_length=100, default=uuid.uuid4,
                          unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['is_read']


def create_profile(instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(owner=instance, name=instance.first_name, username= instance.username)

        mail_subject = 'Welcome to Django Blog'
        mail_message = "You've just created an account on Django blog site, and we are so glad that you're here..."
        user = instance.email

        send_mail(
            mail_subject,
            mail_message,
            settings.EMAIL_HOST_USER,
            [user],
            fail_silently=False,
        )


post_save.connect(create_profile, User)
