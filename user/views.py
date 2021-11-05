from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import UserForm, UserLoginForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import HttpResponseRedirect


User = get_user_model()


def verify_user(request):
    id = request.query_params.get("id")
    obj = get_object_or_404(User, id=id)
    obj.verified = True
    obj.save()
    context = {

    }
    
    return render(request, "user/verified-template.html", context)


class UserRegistrationView(CreateView):
    form_class = UserForm
    success_url = "/"

    def form_valid(self, form):
        return super().form_valid(form)


class UserLoginView(CreateView):
    form_class = UserLoginForm
    success_url = "/"

    def form_valid(self, form):
        email = form.instance.email
        password = form.instance.password
        auth_user = authenticate(email=email, password=password)
        if auth_user:
            login(self.request, auth_user)
            messages.success(self.request, "Logged in")
        else:
            messages.warning(self.request, "Invalid Credentials provided")
            return self.form_invalid(form)

        return HttpResponseRedirect(self.get_success_url())
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

