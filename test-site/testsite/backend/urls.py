from products.views import AccessListView, AccessDetailView
from django.urls import path, re_path


urlpatterns = [
    path('accesses/', AccessListView.as_view(), name='accesses-list'),
    re_path(r'accesses/(?P<pk>[0-9]+)/$', AccessDetailView.as_view(),
           name='access-detail'),

]