from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views.generic import CreateView, DetailView

from user.forms import UserLoginForm, UserRegisterForm

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm
    success_url = ''

class UserRegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = ''


class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
