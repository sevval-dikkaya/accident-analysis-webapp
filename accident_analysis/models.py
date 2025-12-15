from django.db import models

# Create your models here.
class Accidents(models.Model):
    id = models.AutoField(primary_key=True)
    vehicles = models.ManyToManyField('Vehicles', related_name='accidents')
    date_of_accident = models.DateField(blank=True)
    DAMAGE_TYPE_CHOICES = [
        ('unknown', 'Unknown'),
        ('none', 'None'),
        ('minor', 'Minor'),
        ('moderate', 'Moderate'),
        ('major', 'Major'),
    ]
    damage_type = models.CharField(max_length=10, choices=DAMAGE_TYPE_CHOICES, default='minor')
    address_accident = models.PositiveIntegerField(blank=True)

    def __str__(self):
       return f"Accident {self.id} - {self.date_of_accident}"
                 

class Vehicles(models.Model):
    id = models.AutoField(primary_key=True)
    manufacturer_name = models.TextField(blank=True)
    make = models.TextField(blank=True)
    model = models.TextField(blank=True)
    vehicle_year = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.manufacturer_name} - {self.vehicle_year} {self.make} {self.model}"
    