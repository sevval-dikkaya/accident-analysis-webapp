from django import forms
from .models import Accidents, Vehicles

class AccidentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    class Meta:
        model = Accidents
        fields = ['date_of_accident', 'damage_type', 'address_accident', 'vehicles']
        labels = {
            'address_accident': 'Address Accident (Zip Code)',
        }
        widgets = {
            'date_of_accident': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'damage_type': forms.Select(attrs={'class': 'form-select'}),
            'address_accident': forms.TextInput(attrs={
                'class': 'form-control', 
                'pattern': '[0-9]{5}', 
                'maxlength': '5',
                'title': 'Please enter a 5-digit zip code'
            }),
            'vehicles': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True

    class Meta:
        model = Vehicles
        fields = '__all__'
        widgets = {
            'manufacturer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'make': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'vehicle_year': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]{4}',
                'maxlength': '4',
                'title': 'Please enter a 4-digit year'
            }),
        }
