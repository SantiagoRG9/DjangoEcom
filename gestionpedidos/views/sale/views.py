from os import name
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from gestionpedidos.mixin import IsSuperuserMixin
from gestionpedidos.models import Client, Sale
from gestionpedidos.forms import ClientForm, SaleForm
from django.urls import *
from django.contrib.auth.decorators import login_required

class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('saleList')

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':   
                form = self.get_form()
                form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return redirect('clientList')
      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una venta'
        context['list_url'] = reverse_lazy('saleList')
        context['create_url'] = reverse_lazy('saleCreate')
        context['entity'] = 'Ventas'
        context['action'] = 'add'

        return context
