from django.forms import *
from gestionpedidos.models import Category
from gestionpedidos.models import Product, Client

class CategoryForm(ModelForm):
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for form in self.visible_fields():
    #         form.field.widget.attrs['class'] = 'form-control'
    #         form.field.widget.attrs['autocomplete'] = 'off'

    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'nombre': Textarea(
                attrs={
                 'rows' : 3,
                 'cols' : 3
                }
            )
        }


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

        widgets = {
            'name': TextInput(
                attrs={
                 'placeholder' : 'Ingrese nombre'
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()

        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
            
        return data


class TestForm(Form):
    categories = ModelChoiceField(queryset=Category.objects.all(), widget=Select(attrs={
        'class' : 'form-control select2'
    }))

    products = ModelChoiceField(queryset=Product.objects.none(), widget=Select(attrs={
    'class' : 'form-control select2'
    }))


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        widgets = {
            'names' : TextInput(
                attrs=
            )
        }