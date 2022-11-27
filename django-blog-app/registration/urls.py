from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

from .views import PasswordReset, PasswordDone, PasswordConfirm, PasswordComplete

urlpatterns = [
    path('', views.sign_up, name= 'sign-up'),
    path('login/', views.user_login, name= 'login'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name= 'logout'),
    path('change-password/', PasswordReset.as_view(), name="change-password"),
    path('confirm_reset/', PasswordDone.as_view(),
         name='password_reset_done'),
    path('account-reset/<uidb64>/<token>/', PasswordConfirm.as_view(), name='password_reset_confirm'),
    path('password-reset-complet/', PasswordComplete.as_view(), name= 'password-reset-complete')
]
