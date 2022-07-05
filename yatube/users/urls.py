from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordChangeDoneView
)
from django.urls import path
from . import views

app_name = 'users'

logout = 'users/logged_out.html'
login = 'users/login.html'
password_change = 'users/password_change_form.html'
password_change_done = 'users/password_change_done.html'

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
    # path(
    #     'password_change/',
    #     PasswordChangeView.as_view(template_name=password_change),
    #     name='password_change'
    # ),
    path(
        'password_change/done/',
        PasswordChangeDoneView.as_view(template_name=password_change_done),
        name='password_change_done'
    ),
]
