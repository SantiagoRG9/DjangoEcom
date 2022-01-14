from curses import savetty
from django.db import models
from datetime import datetime
from django.db.models.deletion import CASCADE
from django.forms import model_to_dict
from models import BaseModel

# from crum import get_current_user

class Type(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')

    def __str__(self):
        return self.names

class Category(BaseModel):
    names = models.CharField(max_length=150, verbose_name='Nombres', unique=True)
    desc = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripcion')

    def __str__(self):
        return self.names

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     user = get_current_user()
    #     if user and not user.pk:
    #         user = None
    #     if not self.pk:
    #         self.created_by = user
    #     super(Category, self).save()

    def toJSON(self):
        item = model_to_dict(self)
        return item

class Employee(models.Model):
    categ = models.ManyToManyField(Category)
    type = models.ForeignKey(Type, on_delete=CASCADE)
    names = models.CharField(max_length=150, verbose_name='Nombres')
    dni = models.CharField(max_length=150, unique=True, verbose_name='Dni')
    date_joined = models.DateField(default=datetime.now, verbose_name="Fecha de registro")
    date_creation = models.DateTimeField(auto_now=True, verbose_name="")
    date_update = models.DateTimeField(auto_now_add=True, verbose_name="")
    age = models.IntegerField(default=0)
    salary = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    state = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True)
    cvitae = models.FileField(upload_to='avatar/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.names


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre', unique=True)
    cate = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.name



class Client(models.Model):
    names = models.CharField(max_length=150, verbose_name='Nombres')
    surnames = models.CharField(max_length=150, verbose_name='Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name='Dni')
    birthday = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    # gender = models.CharField(max_length=10, choices=gender_choices, blank=True, verbose_name='Direccion')

    def __str__(self):
        return self.names

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Sale(models.Model):
    cli = models.ForeignKey(Client, on_delete=models.CASCADE)
    date_joined = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.cli.names

class DetSale(models.Model):
    sale = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    cant = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.prod.name