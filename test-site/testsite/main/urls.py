from django.urls import path
from .views import *
from django.conf.urls import include


urlpatterns = [
    path('', index, name = 'home'),
]