from django.contrib.gis import admin
from .models import Sentinel

admin.site.register(Sentinel, admin.GeoModelAdmin)