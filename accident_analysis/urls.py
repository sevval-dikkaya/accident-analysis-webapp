from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'api/accidents', views.AccidentViewSet)

urlpatterns = [
    path('', views.accident_list, name='accident_list'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_accident, name='create_accident'),
    path('create-vehicle/', views.create_vehicle, name='create_vehicle'),
    path('export/xlsx/', views.export_accidents_xlsx, name='export_accidents_xlsx'),
    path('', include(router.urls)),
]