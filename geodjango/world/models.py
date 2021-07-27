from django.contrib.gis.db import models
from geo.Geoserver import Geoserver
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime
import environ

# -------------------------------Initialise environment variables-----------------------------
env = environ.Env()
environ.Env.read_env()

###--------------------------------------Trial Model : Can be used to store raster files -------------------------------
# class Elevation(models.Model):
#     name = models.CharField(max_length=100)
#     rast = models.RasterField()

####-------------------------------------Geoserver Initialized-------------------------------------
geo = Geoserver('http://127.0.0.1:'+env('GEOSERVER_PORT')+'/geoserver', username='admin', password='geoserver')


#####-----------------------------Groups of maps from same location--------------------------
class Groups(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

#####----------------------------------Sentinel Model - For Raser Files - Upload FUnction ------------------------------
class Sentinel(models.Model):
    COLOR_RAMPS_CHOICES = [('viridis','viridis'), ('plasma','plasma'), ('inferno', 'inferno'), ('magma', 'magma'), ('cividis', 'cividis'), ('Greys', 'Greys'), ('Purples', 'Purples'), ('Blues', 'Blues'), ('Greens', 'Greens'), ('Oranges', 'Oranges'), ('Reds', 'Reds'), ('YlOrBr', 'YlOrBr'), ('YlOrRd', 'YlOrRd'), ('OrRd', 'OrRd'), ('PuRd', 'PuRd'), ('RdPu', 'RdPu'), ('BuPu', 'BuPu'), ('GnBu', 'GnBu'), ('PuBu', 'PuBu'), ('YlGnBu', 'YlGnBu'), ('PuBuGn', 'PuBuGn'), ('BuGn', 'BuGn'), ('YlGn', 'YlGn'), ('PiYG', 'PiYG'), ('PRGn', 'PRGn'), ('BrBG', 'BrBG'), ('PuOr', 'PuOr'), ('RdGy', 'RdGy'), ('RdBu', 'RdBu'), ('RdYlBu', 'RdYlBu'), ('RdYlGn', 'RdYlGn'), ('Spectral', 'Spectral'), ('coolwarm', 'coolwarm'), ('bwr', 'bwr'), ('seismic', 'seismic')]
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=1000, blank=True)
    file = models.FileField(upload_to='uploads/Raster/%Y/%m/%d')
    color_ramps = models.CharField(max_length=100, choices=COLOR_RAMPS_CHOICES, null=True)
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)
    group_name = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name


    #--------------Publishing to geoserver----------------------
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

    #-------------------Deleting from geoserver------------------------------
@receiver(post_delete, sender=Sentinel)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'App')


######-----------------------------------Change Detection Output--------------------------------------

class ChangeOutputs(models.Model):

    name = models.CharField(max_length=50)
    sentinel_1_id = models.ForeignKey(Sentinel, on_delete=models.CASCADE, null=True, related_name='layer_1')
    sentinel_2_id = models.ForeignKey(Sentinel, on_delete=models.CASCADE, null=True, related_name='layer_2')
    file = models.FileField(upload_to='outputs/change_outputs/%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)
    group_name = models.ForeignKey(Groups, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


    #--------------Publishing to geoserver----------------------
@receiver(post_save, sender=ChangeOutputs)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    name = instance.name
    geo.create_coveragestore(file, workspace='App', layer_name=name)
    geo.create_coveragestyle(file, style_name=name, workspace='App')
    geo.publish_style(layer_name=name, style_name=name, workspace='App')

    #-------------------Deleting from geoserver------------------------------
@receiver(post_delete, sender=ChangeOutputs)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'App')


#######--------------------------------CLustering Output --------------------------------------

class ClusteringOutput(models.Model):

    name = models.CharField(max_length=50)
    sentinel_id = models.ForeignKey(Sentinel, on_delete=models.CASCADE)
    file = models.FileField(upload_to='outputs/cluster_output/%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.name

    #--------------Publishing to geoserver----------------------
@receiver(post_save, sender=ClusteringOutput)
def publish_data(sender, instance, created, **kwargs):
    file = instance.file.path
    name = instance.name
    geo.create_coveragestore(file, workspace='App', layer_name=name)
    geo.create_coveragestyle(file, style_name=name, workspace='App')
    geo.publish_style(layer_name=name, style_name=name, workspace='App')

    #-------------------Deleting from geoserver------------------------------
@receiver(post_delete, sender=ClusteringOutput)
def delete_data(sender, instance, **kwargs):
    geo.delete_layer(instance.name, 'App')