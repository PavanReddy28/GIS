from django.contrib.gis.db import models
from geo.Geoserver import Geoserver
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, null=True)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name

class Zipcode(models.Model):
    code = models.CharField(max_length=5)
    poly = models.PolygonField()

class Elevation(models.Model):
    name = models.CharField(max_length=100)
    rast = models.RasterField()

# initializing the library
geo = Geoserver('http://127.0.0.1:'+env('GEOSERVER_PORT')+'/geoserver', username='admin', password='geoserver')

# The shapefile model
class Sentinel(models.Model):
    COLOR_RAMPS_CHOICES = [('viridis','viridis'), ('plasma','plasma'), ('inferno', 'inferno'), ('magma', 'magma'), ('cividis', 'cividis'), ('Greys', 'Greys'), ('Purples', 'Purples'), ('Blues', 'Blues'), ('Greens', 'Greens'), ('Oranges', 'Oranges'), ('Reds', 'Reds'), ('YlOrBr', 'YlOrBr'), ('YlOrRd', 'YlOrRd'), ('OrRd', 'OrRd'), ('PuRd', 'PuRd'), ('RdPu', 'RdPu'), ('BuPu', 'BuPu'), ('GnBu', 'GnBu'), ('PuBu', 'PuBu'), ('YlGnBu', 'YlGnBu'), ('PuBuGn', 'PuBuGn'), ('BuGn', 'BuGn'), ('YlGn', 'YlGn'), ('PiYG', 'PiYG'), ('PRGn', 'PRGn'), ('BrBG', 'BrBG'), ('PuOr', 'PuOr'), ('RdGy', 'RdGy'), ('RdBu', 'RdBu'), ('RdYlBu', 'RdYlBu'), ('RdYlGn', 'RdYlGn'), ('Spectral', 'Spectral'), ('coolwarm', 'coolwarm'), ('bwr', 'bwr'), ('seismic', 'seismic')]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='uploads/Raster/%Y/%m/%d')
    color_ramps = models.CharField(max_length=100, choices=COLOR_RAMPS_CHOICES, blank=True)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)
    def __str__(self):
        return self.name


@receiver(post_save, sender=Sentinel)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    name = instance.name
    if instance.color_ramps==None:
        '''
        Publish Sentinel file to geoserver using geoserver-rest
        '''
        geo.create_coveragestore(file, workspace='App', layer_name=name)
        geo.create_coveragestyle(file, style_name=name, workspace='App')
        geo.publish_style(layer_name=name, style_name=name, workspace='App')
    else:
        color = instance.color_ramps
        '''
        Publish Sentinel file to geoserver using geoserver-rest
        '''
        geo.create_coveragestore(file, workspace='App', layer_name=name)
        geo.create_coveragestyle(file, style_name=name, workspace='App', color_ramp=color)
        geo.publish_style(layer_name=name, style_name=name, workspace='App')


@receiver(post_delete, sender=Sentinel)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'App')