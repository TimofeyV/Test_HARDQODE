from django.urls import path
from .views import StaticticsViewSet, UserLessonsViewSet, UserProductLessonsViewSet


app_name = 'api'


urlpatterns = [
    
    path('statistics/', StaticticsViewSet.as_view({'get': 'list'})),
    path('user/<int:user_id>/lessons/',
         UserLessonsViewSet.as_view({'get': 'list'}),
         name='user_lessons'),
    path('user/<int:user_id>/product/<int:product_id>/lessons/',
         UserProductLessonsViewSet.as_view({'get': 'list'}),
         name='user_product_lessons'),

]
