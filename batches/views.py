from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Batch, BatchUser
from .forms import BatchCreationForm, BatchUpdateForm, BatchUserForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from .helpers import get_next_batch_classes, get_tomorrow_batch_classes, get_today_batch_classes
from . import helpers
from django.contrib.auth.mixins import LoginRequiredMixin


class BatchListView(ListView):
    template_name = "batch/staff/batch-list.html"
    context_object_name = "batches"

    def get_queryset(self):
        qs = Batch.objects.all()
        return qs


class BatchCreateView(LoginRequiredMixin, CreateView):
    template_name = "batch/staff/batch-create.html"
    form_class = BatchCreationForm
    success_url = "/"

    def form_valid(self, form):
        """
        If form's instance needs to be explicitely set
        """
        return super().form_valid(form)


class BatchUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "batch/staff/batch-create.html"
    form_class = BatchUpdateForm
    lookup_url_kwarg = "id"
    success_url = "/"

    def get_object(self):
        batch_id = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_404(Batch, id=batch_id)
        form = self.get_form()
        form.instance.update = True
        print("Instance update set to True", form)
        return obj

    def form_valid(self, form):
        """
        If form's instance needs to be explicitely set
        """
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class UserClassesView(LoginRequiredMixin, ListView):
    lst = ["next", "previous", "today", "tomorrow"]
    template_name = "batch/user/user_batches_list.html"

    def get_queryset(self):
        qs = get_next_batch_classes(user=self.request.user)
        filter_param = self.request.GET.get("filter", None)
        if filter_param is not None:    
            param = self.filter_keyword(filter_param)
            if param:
                qs = self.get_queryset_on_param(param, qs)

        print("Inside GET QUERYSET ", qs)
        return qs

    def get_queryset_on_param(self, param, qs):

        dictio = {
            "next": self.get_next,
            "previous": self.get_previous,
            "today": get_today_batch_classes,
            "tomorrow": get_tomorrow_batch_classes
        }

        print("Inside get_queryset_on_param ", dictio[param])
        qs = dictio[param](qs=qs)
        return qs

    def get_next(self, qs):
        return qs

    def get_previous(self, qs):
        return qs.filter(started=True)


    def filter_keyword(self, param):
        if param not in self.lst:
            print("Provide Correct Param")
            messages.error(self.request, "Please Provide the correct param")
            return None

        return param


class JoinABatchView(LoginRequiredMixin, DetailView):
    template_name = "batch/user/join_batch.html"
    lookup_url_kwarg = "id"

    def get_batch(self):
        batch_id = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_404(Batch, id=batch_id)
        return obj

    def get_object(self):
        obj = self.get_batch()
        self.curr_object = obj
        return obj

    def get_bkash_form(self):
        pass

    def check_if_user_is_in_batch(self, batch):
        user = self.request.user
        qs = batch.batchuser_set.filter(user=user)
        if qs.exists():
            return qs.get()

        return None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["bkash_form"] = self.get_bkash_form()
        context["is_user_in_batch"] = self.check_if_user_is_in_batch(self.curr_object)
        return context


@login_required
def cancel_batch_join_request(request, batch_id):
    user = request.user
    qs = Batch.objects.filter(id=batch_id)
    if not qs.exists():
        print("Batch not Found")
        return redirect("/")

    batch_obj = qs.get()
    qs = batch_obj.batchuser_set.filter(user=user)
    if not qs.exists():
        print("User is not in batch")
        return redirect("/")

    obj = qs.get()
    obj.delete()
    
    print("Canceled Join Request")
    return redirect("/")

