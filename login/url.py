from django.urls import path
from login.views import *

urlpatterns = [
    path('', LoginFormView2.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]