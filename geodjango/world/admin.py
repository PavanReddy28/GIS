from django.contrib.gis import admin
from .models import Sentinel, WorldBorder, Elevation

admin.site.register(WorldBorder, admin.GeoModelAdmin)
admin.site.register(Elevation, admin.GeoModelAdmin)
admin.site.register(Sentinel, admin.GeoModelAdmin)