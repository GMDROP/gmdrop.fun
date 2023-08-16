from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index2'),
    path('weapon/<id>/', sale),
]