from os import name
# from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.views.generic.edit import FormView
from gestionpedidos.models import Category
from gestionpedidos.forms import CategoryForm
from django.urls import *
from django.contrib.auth.decorators import login_required

def category_list(request):
    data = {
        'title' : 'Listado de categorias',
        'categories' : Category.objects.all()
    }
    return render(request, 'category/list.html', data)


class CategoryListView(ListView):

    model = Category
    template_name = 'category/list.html'
    success_url = reverse_lazy('categoryList')

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     if request.method == 'GET':
    #         return redirect('category_list2')
    #     return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Category.objects.all():
                    data.append(i.toJSON())
                else:
                    data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe= False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de categorias'
        context['create_url'] = reverse_lazy('categoryCreate')
        return context


class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('categoryList')

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
        return redirect('categoryList')
      
       
        # cat = Category.objects.get(pk=request.POST['id'])
        # data['name'] = cat.names 
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creacion de una categoria'
        context['list_url'] = reverse_lazy('categoryList')
        context['create_url'] = reverse_lazy('categoryCreate')
        context['entity'] = 'Categorias'
        context['action'] = 'add'

        return context


class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('categoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una categoria'
        context['action'] = 'edit'
        context['list_url'] = reverse_lazy('categoryList')
        context['entity'] = 'Categorias'

        return context


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "category/delete.html"
    success_url = reverse_lazy('categoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminacion de una categoria'
        context['list_url'] = reverse_lazy('categoryList')
        context['entity'] = 'Categorias'

        return context


class CategoryFormView(FormView):
    form_class = CategoryForm
    template_name = 'category/create.html'
    success_url = reverse_lazy('categoryList')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Categoria'
        context['list_url'] = reverse_lazy('categoryList')
        context['entity'] = 'Categorias'
        context['action'] = 'add'

        return context

    def clean(self):
        cleaned = super().clean()
        if len(cleaned['name']) <= 50:
            self.add_error('name', 'le faltan caracteres')
        return cleaned