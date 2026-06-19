from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from rest_framework.reverse import reverse_lazy

from user.forms import UserLoginForm, UserRegisterForm

class UserLoginView(LoginView):
    template_name = 'user/login.html'
    form_class = UserLoginForm

class UserRegisterView(CreateView):
    template_name = 'user/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')


class UserProfileView(DetailView):
    model = get_user_model()
    template_name = 'user/profile.html'
    context_object_name = 'user'
    pk_url_kwarg = 'user_id'
