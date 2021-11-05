from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from .forms import UserForm

User = get_user_model()

def verify_user(request):
    id = request.query_params.get("id")
    obj = get_object_or_404(User, id=id)
    obj.verified = True
    obj.save()
    context = {

    }
    
    return render(request, "user/verified-template.html", context)