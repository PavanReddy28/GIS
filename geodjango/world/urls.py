from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('cluster', views.cluster, name="cluster"),
    path('change', views.change, name="change"),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
]
