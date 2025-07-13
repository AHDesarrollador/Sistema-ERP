from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/data/', views.dashboard_api_data, name='dashboard-api-data'),
]