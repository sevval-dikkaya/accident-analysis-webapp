from .models import Accidents
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import AccidentSerializer
import openpyxl

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

class AccidentViewSet(viewsets.ModelViewSet):
    queryset = Accidents.objects.all().order_by('-date_of_accident')
    serializer_class = AccidentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AccidentFilter


