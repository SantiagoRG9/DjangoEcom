from multiprocessing import context
from re import template
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from gestionpedidos.forms import TestForm
from gestionpedidos.models import Product

class TestView(TemplateView):
    template_name = 'test.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try: 
            action = request.POST['action']
            if action == 'search_product_id':
                data = []
                for i in Product.objects.filter(cat_id=request.POST['id']):
                    data.append({'id' : i.id, 'name' : i.name})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Select Anidados | Django'
        context['form'] = TestForm()
        return context