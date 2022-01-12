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
from homepages.views import *
from login.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('erp/', CategoryListView.as_view(), name='categoryList'),
    path('erp2/', CategoryCreateView.as_view(), name='categoryCreate'),
    path('erp3/<int:pk>', CategoryUpdateView.as_view(), name='categoryUpdate'),
    path('erp4/<int:pk>', CategoryDeleteView.as_view(), name='categoryDelete'),
    path('form/', CategoryFormView.as_view(), name='categoryForm'),

    # HOMEPAGES
    path('', IndexView.as_view()),

    #LOGIN
    path('login/', LoginFormView.as_view()),

]
