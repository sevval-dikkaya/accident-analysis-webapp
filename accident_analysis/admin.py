from django.contrib import admin
from .models import Accidents, Vehicles

class AccidentsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_of_accident', 'damage_type')
    filter_horizontal = ('vehicles',)

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'manufacturer_name', 'make', 'model', 'vehicle_year')

# Register your models here.
admin.site.register(Accidents, AccidentsAdmin)
admin.site.register(Vehicles, VehicleAdmin)