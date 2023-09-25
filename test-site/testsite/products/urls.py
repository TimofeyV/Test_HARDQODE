from django.urls import path
from .views import *


app_name = 'products'

urlpatterns = [
    path('', catalog, name = 'catalog'),
    path('<int:product_id>', lessons, name = 'lesson_list'),
    path('<int:product_id>/<int:lesson_id>', lesson_detail, name = 'lesson_detail'),
    path('video_moment/', video_moment, name='video_moment'),
]