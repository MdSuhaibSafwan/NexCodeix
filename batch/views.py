from django.shortcuts import get_object_or_404, render
from django.contrib.auth import get_user_model
from .models import Batch, BatchUser
from .forms import BatchCreationForm, BatchUpdateForm, BatchUserForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.views.generic import ListView, CreateView, UpdateView, DetailView


class BatchListView(ListView):
    template_name = "batch/staff/batch-list.html"
    context_object_name = "batches"

    def get_queryset(self):
        qs = Batch.objects.all()
        return qs


class BatchCreateView(CreateView):
    template_name = "batch/staff/batch-create.html"
    form_class = BatchCreationForm
    success_url = "/"

    def form_valid(self, form):
        """
        If form's instance needs to be explicitely set
        """
        return super().form_valid(form)


class BatchUpdateView(UpdateView):
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
