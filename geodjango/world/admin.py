from django.contrib.gis import admin
from .models import Sentinel, Elevation

admin.site.register(Elevation, admin.GeoModelAdmin)
admin.site.register(Sentinel, admin.GeoModelAdmin)