from django.urls import path
from .views import *

urlpatterns = [
    path('create/', case_create, name='case_create'),
    path('<id>/', case, name='case'),
    path('get_price/<id>/', get_price),
]
