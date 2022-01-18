from datetime import datetime
from django.forms import *
from gestionpedidos.models import Category, Sale
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
                attrs={
                    'placeholder' : 'Ingrese sus nombres',
                }
            ),
            'surnames' : TextInput(
                attrs={
                    'placeholder' : 'Ingrese sus apellidos',
                }
            ),
            'dni' : TextInput(
                attrs={
                    'placeholder' : 'Ingrese su dni',
                }
            ),
            'birthday' : DateInput(
                attrs={
                    'value' : datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'address' : TextInput(
                attrs={
                    'placeholder' : 'Ingrese su direccion',
                }
            ),
        }


class SaleForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'

        self.fields['cli'].widget.attrs['autofocus'] = True
        self.fields['cli'].widget.attrs['autocomplete'] = 'form-control select2'
        self.fields['cli'].widget.attrs['style'] = 'width: 100%'

        self.fields['date_joined'].widget.attrs = {
            'autocomplete' : 'off',
            'class' : 'form-control datetimepicker-input',
            'id' : 'date_joined',
            'data-target' : '#date_joined',
            'data-toggle' : 'datetimepicker'
        }

        self.fields['subtotal'].widget.attrs = {
            'readonly' : True,
            'class' : 'form-control',
        }

        self.fields['total'].widget.attrs = {
            'readonly' : True,
            'class' : 'form-control',
        }

    class Meta:
        model = Sale
        fields = '__all__'
        widgets = {
            'cli' : Select(attrs={
                'class' : 'form-control select2',
                'style' : 'width: 100%'
            }),
            'date_joined' : DateInput(
                attrs={
                    'value' : datetime.now().strftime('%Y-%m-%d'),
                }
            ),
                 'date_joined' : DateInput(
                attrs={
                    'value' : datetime.now().strftime('%Y-%m-%d'),
                }
            ),
                 'subtotal' : NumberInput(
                attrs={
                    'value' : '0,0',
                }
            ),
                  'iva' : NumberInput(
                attrs={
                    'value' : '0,0',
                }
            ),
                  'total' : NumberInput(
                attrs={
                    'value' : '0,0',
                }
            ),
        }
