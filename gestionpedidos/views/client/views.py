from os import name
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from gestionpedidos.mixin import IsSuperuserMixin
from gestionpedidos.models import Client
from gestionpedidos.forms import ClientForm
from django.urls import *
from django.contrib.auth.decorators import login_required

def client_list(request):
    data = {
        'title' : 'Listado de clientes',
        'clients' : Client.objects.all()
    }
    return render(request, 'client/list.html', data)


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'gestionpedidos.view_client'
    model = Client
    template_name = 'client/list.html'
    success_url = reverse_lazy('clientList')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

        

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         return redirect('client_list2')
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Client.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de clientes'
        context['create_url'] = reverse_lazy('clientCreate')
        return context


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('clientList')

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
      
       
        # cat = client.objects.get(pk=request.POST['id'])
        # data['name'] = cat.names 
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de un cliente'
        context['list_url'] = reverse_lazy('clientList')
        context['create_url'] = reverse_lazy('clientCreate')
        context['entity'] = 'Clientes'
        context['action'] = 'add'

        return context


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('clientList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un cliente'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('clientList')
        context['entity'] = 'Clientes'

        return context


class ClientDeleteView(DeleteView):
    model = Client
    template_name = "client/delete.html"
    success_url = reverse_lazy('clientList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de un cliente'
        context['list_url'] = reverse_lazy('clientList')
        context['entity'] = 'Clientes'

        return context


class ClientFormView(FormView):
    form_class = ClientForm
    template_name = 'client/create.html'
    success_url = reverse_lazy('clientList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Cliente'
        context['list_url'] = reverse_lazy('clientList')
        context['entity'] = 'Clientes'
        context['action'] = 'add'

        return context

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 50:
            self.add_error('name', 'le faltan caracteres')
        return cleaned