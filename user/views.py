from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import UserForm, UserLoginForm
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.http import HttpResponseRedirect, Http404


User = get_user_model()


def verify_user(request):
    query_id = request.GET.get("id")
    # query_id = 2
    if not query_id:
        raise Http404("No Id is given to the url")
    obj = get_object_or_404(User, id=query_id)
    if obj.verified:
        verified = True
    else:
        obj.verified = True
        obj.save()
        verified = "verifying"
    context = {
        "verified": verified,
    }
    
    return render(request, "user/verified-template.html", context)


class UserRegistrationView(CreateView):
    form_class = UserForm
    success_url = "/"
    template_name = "user/auth/registration.html"

    def form_valid(self, form):
        form_obj = form.save(commit=False)
        self.object = form_obj
        print("Form Object ", form_obj)
        password = form.cleaned_data.get("password")
        print("password ", password)
        form_obj.set_password(password)
        form_obj.save()
        return HttpResponseRedirect(self.get_success_url())



