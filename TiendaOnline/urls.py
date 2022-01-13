"""TiendaOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from gestionpedidos.views.category.views import *
from gestionpedidos.views.product.views import *
from homepages.views import *
from login.views import *
from gestionpedidos.views.dashboard.views import DashboardView

urlpatterns = [

    # CATEGORY
    path('admin/', admin.site.urls),
    path('erp/', CategoryListView.as_view(), name='categoryList'),
    path('erp2/', CategoryCreateView.as_view(), name='categoryCreate'),
    path('erp3/<int:pk>', CategoryUpdateView.as_view(), name='categoryUpdate'),
    path('erp4/<int:pk>', CategoryDeleteView.as_view(), name='categoryDelete'),
    path('formcate/', CategoryFormView.as_view(), name='categoryForm'),

    # PRODUCT
    path('prod/', ProductListView.as_view(), name='productList'),
    path('prod2/', ProductCreateView.as_view(), name='productCreate'),
    path('prod3/<int:pk>', ProductUpdateView.as_view(), name='productUpdate'),
    path('prod4/<int:pk>', ProductDeleteView.as_view(), name='productDelete'),
    path('formprod/', ProductFormView.as_view(), name='productForm'),





    # HOMEPAGES
    path('', IndexView.as_view(), name='homepage'),

    #LOGIN
    path('login/', include('login.url')),

    # DASHBOARD
    path('dash', DashboardView.as_view(), name='dashboard'),

]
