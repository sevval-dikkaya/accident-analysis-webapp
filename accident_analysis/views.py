from .models import Accidents
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import AccidentSerializer
from .forms import AccidentForm, VehicleForm
import openpyxl
import json
from django.db.models import Count
from django.db.models.functions import TruncMonth

class AccidentFilter(filters.FilterSet):
    manufacturer = filters.CharFilter(field_name='vehicles__manufacturer_name', lookup_expr='icontains')
    damage_type = filters.ChoiceFilter(choices=Accidents.DAMAGE_TYPE_CHOICES)
    address_accident = filters.NumberFilter()
    date_of_accident = filters.DateFilter()

    class Meta:
        model = Accidents
        fields = ['damage_type', 'address_accident', 'date_of_accident']

# Create your views here.
def accident_list(request):
    queryset = Accidents.objects.prefetch_related('vehicles').all().order_by('-date_of_accident')
    accident_filter = AccidentFilter(request.GET, queryset=queryset)
    
    return render(request, 'accident_analysis/accident_list.html', {
        'filter': accident_filter,
        'accidents': accident_filter.qs
    })

def export_accidents_xlsx(request):
    queryset = Accidents.objects.prefetch_related('vehicles').all().order_by('-date_of_accident')
    accident_filter = AccidentFilter(request.GET, queryset=queryset)
    accidents = accident_filter.qs

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="accident_report.xlsx"'

    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Accidents'

    # Header row
    columns = ['ID', 'Date', 'Damage Type', 'Zip Code', 'Vehicles']
    worksheet.append(columns)

    for accident in accidents:
        vehicles_str = ", ".join([f"{v.vehicle_year} {v.manufacturer_name} {v.model}" for v in accident.vehicles.all()])
        row = [
            accident.id,
            accident.date_of_accident,
            accident.get_damage_type_display(),
            accident.address_accident,
            vehicles_str
        ]
        worksheet.append(row)

    workbook.save(response)
    return response

def dashboard(request):
    # Damage Type Stats
    damage_stats = Accidents.objects.values('damage_type').annotate(count=Count('id'))
    damage_labels = [item['damage_type'] for item in damage_stats]
    damage_counts = [item['count'] for item in damage_stats]
    
    # Accidents over time (by month)
    time_stats = Accidents.objects.annotate(month=TruncMonth('date_of_accident')).values('month').annotate(count=Count('id')).order_by('month')
    time_labels = [item['month'].strftime('%Y-%m') if item['month'] else 'Unknown' for item in time_stats]
    time_counts = [item['count'] for item in time_stats]

    # Manufacturer Stats (Top 10)
    manufacturer_stats = Accidents.objects.values('vehicles__manufacturer_name').annotate(count=Count('id')).order_by('-count')[:10]
    manufacturer_labels = [item['vehicles__manufacturer_name'] if item['vehicles__manufacturer_name'] else 'Unknown' for item in manufacturer_stats]
    manufacturer_counts = [item['count'] for item in manufacturer_stats]

    return render(request, 'accident_analysis/dashboard.html', {
        'damage_labels': json.dumps(damage_labels),
        'damage_counts': json.dumps(damage_counts),
        'time_labels': json.dumps(time_labels),
        'time_counts': json.dumps(time_counts),
        'manufacturer_labels': json.dumps(manufacturer_labels),
        'manufacturer_counts': json.dumps(manufacturer_counts),
    })

def create_accident(request):
    if request.method == 'POST':
        form = AccidentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accident_list')
    else:
        form = AccidentForm()
    return render(request, 'accident_analysis/create_accident.html', {'form': form})

def create_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect back to accident creation if that's where they came from, or list
            return redirect('create_accident')
    else:
        form = VehicleForm()
    return render(request, 'accident_analysis/create_vehicle.html', {'form': form})

class AccidentViewSet(viewsets.ModelViewSet):
    queryset = Accidents.objects.all().order_by('-date_of_accident')
    serializer_class = AccidentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AccidentFilter


