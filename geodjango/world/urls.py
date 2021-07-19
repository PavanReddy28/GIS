from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('clustering/<int:id>/', views.cluster, name="cluster"),
    path('changedetection', views.change, name="change"),
    path('upload', views.upload, name='upload'),
    path('search', views.search, name='search'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
