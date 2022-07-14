# Импортируем CreateView, чтобы создать ему наследника
# from django.contrib.auth.views import PasswordChangeView
# Функция reverse_lazy позволяет
# получить URL по параметрам функции path()
from django.urls import reverse_lazy
from django.views.generic import CreateView

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, PasswordChangeForm


class SignUp(CreateView):
    form_class = CreationForm
    # После успешной регистрации перенаправляем пользователя на главную.
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'


# class PasswordChanging(PasswordChangeView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('users:password_change_done')
#     template_name = 'users/password_change_form.html'
