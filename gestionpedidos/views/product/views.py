from os import name
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from gestionpedidos.models import Product, Product
from gestionpedidos.forms import *
from django.urls import *
from django.contrib.auth.decorators import login_required

class ProductListView(ListView):

    model = Product
    form_class = ProductForm
    template_name = 'product/list.html'

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
                for i in Product.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de productos'
        context['create_url'] = reverse_lazy('productCreate')
        return context


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('productList')

    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opcion'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)
      
       
        # cat = Product.objects.get(pk=request.POST['id'])
        # data['name'] = cat.names 
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una producto'
        context['list_url'] = reverse_lazy('productList')
        context['create_url'] = reverse_lazy('productList')
        context['entity'] = 'Productos'
        context['action'] = 'add'

        return context


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('productList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de un producto'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('productList')
        context['entity'] = 'Productos'

        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = "product/delete.html"
    success_url = reverse_lazy('productList')

    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try: 
            self.get_object
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de un producto'
        context['list_url'] = reverse_lazy('productList')
        context['entity'] = 'Productos'

        return context


class ProductFormView(FormView):
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('productList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Producto'
        context['list_url'] = reverse_lazy('productList')
        context['entity'] = 'Productos'
        context['action'] = 'add'

        return context

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 50:
            self.add_error('name', 'le faltan caracteres')
        return cleaned