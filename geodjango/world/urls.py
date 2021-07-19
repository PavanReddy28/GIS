from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('clustering/<int:id>/', views.cluster, name="cluster"),
    path('changedetection', views.change, name="change"),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
]
