from django.shortcuts import render
from django.contrib.auth import views as auth_view
from django.urls import reverse_lazy
from .forms import AuthenticationForm
# Create your views here.

class LoginView(auth_view.LoginView):

    template_name = "accounts/login.html"
    form_class = AuthenticationForm
    redirect_authenticated_user = True


class LogoutView(auth_view.LogoutView):
    pass
