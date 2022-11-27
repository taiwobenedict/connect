from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from posts.forms import CommentForm, PostForm, ProfileForm, MessageForm
from .models import Comment, Message, Post, Profile
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.template import defaultfilters
from .utils import search
from PIL import Image

from Blog import settings

# Create your views here.

# <=== Home View ===>
#  Renders All Posts


@login_required(login_url='login')
def index(request):

    profile = get_object_or_404(Profile, owner=request.user)
    current_page = 1
    search_value = ''
    unread_messages = Message.objects.filter(
        reciever=request.user.profile, is_read=False).count()

    # if 'search' and 'page' in request.GET.keys():

    if request.GET.get('search'):
        paginator = search(request)['paginator']
        search_value = search(request)['search_value']
        
    else:
        all_posts = Post.objects.all()
        paginator = Paginator(all_posts, 3)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        current_page = request.GET.get('page')
        try:
            posts = paginator.page(current_page)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        except PageNotAnInteger:
            posts = paginator.page(1)

        data = []
        for post in posts:
            data.append({
                'post_id': post.id,
                'profile_id': post.owner.profile.id,
                'profile_image': post.owner.profile.ProfileImageUrl(),
                'username': defaultfilters.title(post.owner.username),
                'date': defaultfilters.date(post.created, 'M j, Y, g:i a'),
                'title':post.title,
                'post_image': post.ImageUrl(),
                'post_image_name': post.image.name,
                'body': defaultfilters.linebreaksbr(post.body),
                'comment': post.comments.all().count(),
                'total_liked': post.total_likes(),
                'user_liked': post.likes.filter(id=request.user.id).exists()

            })

        return JsonResponse([data, {"page_has_next": posts.has_next()}], safe=False)

    post_form = PostForm()
    context = {
        'posts': paginator.page(current_page),
        'profile': profile,
        'search': search_value,
        'paginator': paginator,
        'postForm': post_form,
        'unread_messages': unread_messages
    }
    return render(request, 'posts/home.html', context)

# <=== Profile View ===>
# Renders Logged-in User Profile


@login_required(login_url='login')
def own_profile(request):
    profile = get_object_or_404(Profile, owner=request.user)
    context = {
        'profile': profile,
        'page': 'own-profile'
    }
    return render(request, 'posts/profile.html', context)

# <=== Profile View ===>
# Renders Users Profile


@login_required(login_url='login')
def user_profile(request, id):
    message_form = MessageForm()
    profile = get_object_or_404(Profile, pk=id)
    context = {
        'profile': profile,
        'messageForm': message_form,
    }
    return render(request, 'posts/profile.html', context)

# <=== Post Details View ===>


@login_required(login_url='login')
def post_details(request, id):
    form = CommentForm()
    post = get_object_or_404(Post, pk=id)
    post_form = PostForm(instance=post)
    comments = Comment.objects.filter(post=post).order_by('-created')

    if request.method == 'POST':
        comment =  json.load(request)['comment']
        form = CommentForm({'body': comment})
        if form.is_valid():
            x = form.save(commit=False)
            x.post = post
            x.owner = request.user
            x.save()
            form = CommentForm()  # show empty form

            #  Get comment instance
            data = {
                "image": x.owner.profile.ProfileImageUrl(),
                "owner": defaultfilters.title(x.owner.username),
                "created": defaultfilters.date(x.created, 'M. j, Y, g a'),
                "body": x.body,
                "id": x.owner.profile.id
            }

            return JsonResponse(data)
    context = {
        'post': post,
        'commentForm': form,
        'comments': comments,
        'postForm': post_form
    }
    return render(request, 'posts/post.html', context)


@login_required(login_url='login')
# <=== Post Udating View ===>
def post_update(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            x =post_form.save(commit=False)
            x.post = post
            x.owner = request.user
            x.save()
            return redirect('post-details', id)
    post_form = PostForm(instance=post)
    context = {
        'postForm': post_form,
        'page': 'update-post',
        'post': post,
    }
    return render(request, 'posts/post.html', context)


# <=== Profile Udating View ===>
@login_required(login_url='login')
def update_profile(request, id):
    profile = get_object_or_404(Profile, pk=id)
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect('user-profile', id)
    context = {
        'profile': profile,
        'form': form
    }
    return render(request, 'posts/profile_edit.html', context)


# <=== Add New Post ===>
@login_required(login_url='login')
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            return redirect('index')
    form = PostForm()
    context = {
        'postForm': form,
        'page': 'add-post'
    }
    return render(request, 'posts/home.html', context)


# <=== Edit Post ===>
@login_required(login_url='login')
def edit_post(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('index')
    form = PostForm(instance=post)
    context = {
        'form': form,
        'page': 'update-post'
    }
    return render(request, 'posts/profile_post_update.html', context)


@login_required(login_url='login')
def likes(request):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        like_id = json.load(request)['id']
        liked_post = get_object_or_404(Post, pk=like_id)
        liked = liked_post.likes.filter(id=request.user.id).exists()
        if liked:
            liked_post.likes.remove(request.user)
        else:
            liked_post.likes.add(request.user)
        total_likes = liked_post.likes.count()
        return JsonResponse({'total_likes': total_likes, 'liked': liked})
    else:
        return redirect('index')

# <=== Delete Post ===>


@login_required(login_url='login')
def delete_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('index')


@login_required(login_url='login')
def inbox(request):
    inbox_messages = Message.objects.filter(reciever=request.user.profile)
    sent_messages = Message.objects.filter(sender= request.user).order_by('-created')
    unread_messages = Message.objects.filter(
        reciever = request.user.profile, is_read = False).count()
    context = {
        'all_messages': inbox_messages,
        'page': 'inbox',
        'total_unread': unread_messages,
        'sent_messages': sent_messages
    }
    return render(request, 'posts/inbox.html', context)


@login_required(login_url='login')
def message_form(request, id):
    form = MessageForm()
    receiver_profile = Profile.objects.get(pk=id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.reciever = receiver_profile
            form.save()
            messages.success(
                request, f'Message sent successfully to {receiver_profile.owner.username}')
            form = MessageForm()
            return redirect('inbox')

    context = {
        'form': form,
    }
    return render(request, 'posts/message.html', context)


@login_required(login_url='login')
def message_detail(request, id):
    message = Message.objects.get(pk=id)
    message.is_read = True
    message.save()
    context = {
        'page': 'message_detail',
        'message': message,
        'form': MessageForm()
    }
    return render(request, 'posts/message_detail.html', context)
