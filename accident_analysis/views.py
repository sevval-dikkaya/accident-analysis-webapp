from django.shortcuts import render
from .models import Accidents

# Create your views here.
def accident_list(request):
    accidents = Accidents.objects.prefetch_related('vehicles').all().order_by('-date_of_accident')
    return render(request, 'accident_analysis/accident_list.html', {'accidents': accidents})
