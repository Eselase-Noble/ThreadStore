from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime


class LoginView(View):
    template = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template, context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user.last_login = datetime.datetime.now()
            messages.success(request, 'Hi there, {}'.format(user.name))
            return redirect('backend:dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('accounts:login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('accounts:login')
