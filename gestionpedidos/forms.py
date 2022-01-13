from django.forms import *
from gestionpedidos.models import Category
from gestionpedidos.models import Product

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
