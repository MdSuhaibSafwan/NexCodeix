import json
from django.http.response import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Batch, BatchClass, BatchUser, ClassJoinedUser
from .forms import BatchCreationForm, BatchUpdateForm, BatchUserForm
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied, ValidationError
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from .helpers import get_next_batch_classes, get_tomorrow_batch_classes, get_today_batch_classes
from . import helpers
from .mixins import LoginRequiredAndVerificationMixin,login_and_verification_required
from django.db.utils import IntegrityError
from rest_framework.authtoken.models import Token


class BatchListView(LoginRequiredAndVerificationMixin, ListView):
    template_name = "batch/staff/batch-list.html"
    context_object_name = "batches"

    def get_queryset(self):
        qs = Batch.objects.all()
        return qs


class BatchCreateView(LoginRequiredAndVerificationMixin, CreateView):
    template_name = "batch/staff/batch-create.html"
    form_class = BatchCreationForm
    success_url = "/"

    def form_valid(self, form):
        """
        If form's instance needs to be explicitely set
        """
        return super().form_valid(form)


class BatchUpdateView(LoginRequiredAndVerificationMixin, UpdateView):
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


class BatchDetailView(LoginRequiredAndVerificationMixin, DetailView):
    template_name = "batch/staff/batch-create.html"
    lookup_url_kwarg = "id"

    def get_object(self):
        batch_id = self.kwargs.get(self.lookup_url_kwarg)
        obj = get_object_or_404(Batch, id=batch_id)
        form = self.get_form()
        form.instance.update = True
        print("Instance update set to True", form)
        return obj
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, *args, **kwargs):
        anouncement = self.request.GET.get("anouncement_field")
        context = self.get_context_data(request=self.request, user=self.request.user)
        if anouncement:
            print("Creating Anouncement for ", anouncement)

        return render(self.request, self.template_name, context=context)
    


class UserClassesView(LoginRequiredAndVerificationMixin, ListView):
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


class JoinABatchView(LoginRequiredAndVerificationMixin, DetailView):
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


@login_and_verification_required
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


class ClassDetailView(DetailView):
    template_name = "batch/user/class_detail.html"
    context_object_name = "class_obj"
    lookup_url_kwarg = "class_id"
    
    def get_queryset(self):
        return BatchClass.objects.none()

    def get_object(self):
        obj = get_object_or_404(BatchClass, id=self.kwargs.get(self.lookup_url_kwarg))
        self.object = obj
        return obj

    def get_user_token(self):
        obj, created = Token.objects.get_or_create(user=self.request.user)
        return obj.key

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_url"] = f"/batch/user/class/{self.kwargs.get(self.lookup_url_kwarg)}/view/"
        context["user_token"] = str(self.get_user_token())
    
        return context

    def post(self, *args, **kwargs):
        batch_class_obj = self.get_object()
        self.object = batch_class_obj
        curr_user = self.request.user
        data = json.loads(self.request.body)
        
        is_ajax = data.get("is_ajax")
        is_joining_batch = data.get("joining")

        self.view_url = f"/batch/user/class/{self.kwargs.get(self.lookup_url_kwarg)}/view/"

        resp_data = {}

        if is_joining_batch:
            batch = batch_class_obj.batch
            qs = batch.batchuser_set.filter(user=curr_user)
            print("BATCH QS --> ", qs)
        
            if not qs.exists():
                resp_data["joining_status"] = "Not in this Batch"
                return JsonResponse(resp_data)

            # batch_user = qs.get()
            # if not batch_user.is_verified:
            #     resp_data["joining_status"] = "Not verified for this Batch"
            #     return JsonResponse(resp_data)
            try:
                class_joined_obj = ClassJoinedUser.objects.create(batch_class=batch_class_obj, user=curr_user, status="P")
            except IntegrityError as e:
                print(e)
                return JsonResponse(resp_data)

            resp_data["batch_class_id"] = str(class_joined_obj.id)
            resp_data["user"] = curr_user.email
            resp_data["joining_status"] = "pending"

        if is_ajax:
            print("RETURNING JSON RESPONSE")
            resp_data["status"] = "ok"
            return JsonResponse(resp_data)

        return HttpResponseRedirect(self.view_url)

