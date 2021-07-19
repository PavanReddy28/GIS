from django.contrib.gis import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('world.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
