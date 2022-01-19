from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from reports.forms import ReportForm

from http.client import HTTPResponse
import json
from os import name
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse,HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from gestionpedidos.mixin import IsSuperuserMixin
from gestionpedidos.models import Client, Product, Sale
from gestionpedidos.forms import ClientForm, SaleForm
from django.urls import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

from user.models import User

class UserChangePassword(FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'changepassword.html'
    success_url = reverse_lazy('login')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        return form

    def post(self, request, *args, **kwargs):  
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':   
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edicion de password'
        context["list_url"] = reverse_lazy('')
        context["title"] = 'Reporte de ventas'
        context["form"] = ReportForm()
        return context