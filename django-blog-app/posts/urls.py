
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name= 'index'),
    path('profile', views.own_profile, name= 'own-profile'),
    path('user_profile/<str:id>/', views.user_profile, name= 'user-profile'),
    path('post_details/<str:id>/', views.post_details, name= 'post-details'),
    path('update_post/<str:id>/', views.post_update, name= 'update-post'),
    path('update_profiel/<str:id>/', views.update_profile, name= 'update-profile'),
    path('add_post/', views.add_post, name= 'add-post'),
    path('edit_post/<str:id>/', views.edit_post, name='edit-post'),
    path('like_post/', views.likes, name= 'like-post'),
    # path('comment/<str:id>/', views.post_comment, name= 'comment'),
    path('delete_post/<str:id>/', views.delete_post, name= 'delete-post'),
    path('inbox/', views.inbox, name= 'inbox'),
    path('message/<str:id>/', views.message_form, name= 'message'),
    path('message-detail/<str:id>/', views.message_detail, name= 'message-detail'),
]