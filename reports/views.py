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

class ReportSaleView(TemplateView):
    template_name = 'report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':   
                data = [] 
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Sale.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date])
            for s in search:
                    data.append([
                        s.id,
                        s.cli.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
      

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Reporte de ventas'
        context["list_url"] = reverse_lazy('')
        context["title"] = 'Reporte de ventas'
        context["form"] = ReportForm()
        return context
    
