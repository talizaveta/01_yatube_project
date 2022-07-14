from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeDoneView,
                                       PasswordChangeView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.urls import path

from . import views

app_name = 'users'

logout = 'users/logged_out.html'
login = 'users/login.html'
password_change = 'users/password_change_form.html'
password_change_done = 'users/password_change_done.html'
password_reset = 'users/password_reset_form.html'
password_reset_done = 'users/password_reset_done.html'
password_reset_confirm = 'users/password_reset_confirm.html'
password_reset_complete = 'users/password_reset_complete.html'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path(
        'login/',
        LoginView.as_view(template_name=login),
        name='login'
    ),
    path(
        'logout/',
        LogoutView.as_view(template_name=logout),
        name='logout'
    ),
    path(
        'password_change/',
        PasswordChangeView.as_view(template_name=password_change),
        name='password_change'
    ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name=password_change_done),
        name='password_change_done'
    ),
    path(
        'password_reset/',
        PasswordResetView.as_view(template_name=password_reset),
        name='password_reset'
    ),
    path(
        'password_reset/done/',
        PasswordResetDoneView.as_view(template_name=password_reset_done),
        name='password_reset_done'
    ),
    path(
        'password_reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name=password_reset_confirm),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        PasswordResetCompleteView.as_view(template_name=password_reset_complete),
        name='password_reset_complete'
    ),
]
