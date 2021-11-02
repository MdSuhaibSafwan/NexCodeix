from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Batch, BatchUser
from .forms import BatchForm, BatchUserForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.views.generic import ListView, CreateView, UpdateView, DetailView



