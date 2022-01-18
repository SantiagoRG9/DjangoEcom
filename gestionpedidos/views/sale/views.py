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

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders



class SaleListView(ListView):

    model = Sale
    form_class = SaleForm
    template_name = 'sale/list.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         return redirect('product_list2')
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Sale.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de ventas'
        context['create_url'] = reverse_lazy('saleCreate')
        return context


class SaleCreateView(CreateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('saleList')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':   
               data = [] 
               prods = Product.objects.filter(request.POST['term'])
               for i in prods:
                   item = i.toJSON()
                   item['value'] = i.name
                   data.append(item)
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una venta'
        context['list_url'] = reverse_lazy('saleList')
        context['create_url'] = reverse_lazy('saleCreate')
        context['entity'] = 'Ventas'
        context['action'] = 'add'

        return context


class SaleUpdateView(UpdateView):
    model = Sale
    form_class = SaleForm
    template_name = 'sale/create.html'
    success_url = reverse_lazy('saleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una venta'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('saleList')
        context['entity'] = 'Ventas'

        return context


class SaleDeleteView(DeleteView):
    model = Sale
    template_name = "sale/delete.html"
    success_url = reverse_lazy('saleList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de una venta'
        context['list_url'] = reverse_lazy('saleList')
        context['entity'] = 'Ventas'

        return context


class SaleInvoicePdfView(View):
    def get(self, request, *args, **kwargs):

        try:
            template = get_template('sale/invoice.html')
            context = {
                'sale' : Sale.objects.get(pk=self.kwargs['pk']),
                'comp' : {'name' : 'OneA Corporation','ruc' : '9999999','address' : 'Cali, Colombia'},
                # 'icon' : '{}{}'.format(settings.STATIC_URL, 'img/anarquia.ico')
                }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            
            pisa_status = pisa.CreatePDF(
                html, dest=response
                # link_callback=self.link_callback
            )
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('saleList'))
