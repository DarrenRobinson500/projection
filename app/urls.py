from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('projection', projection, name='projection'),
    path('new_variable', new_variable, name='new_variable'),
    path('edit_variable/<id>', edit_variable, name='edit_variable'),
    path('delete_variable/<id>', delete_variable, name='delete_variable'),
    ]
