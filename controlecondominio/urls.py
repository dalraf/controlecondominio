from django.urls import path
from controlecondominio.views import *

urlpatterns = [
    path('', index,)
]