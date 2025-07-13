from django.urls import path
from . import views

app_name = 'sales'

urlpatterns = [
    # Customers
    path('customers/', views.CustomerListCreateView.as_view(), name='customer-list'),
    path('customers/<int:pk>/', views.CustomerDetailView.as_view(), name='customer-detail'),
    
    # Sales
    path('sales/', views.SaleListCreateView.as_view(), name='sale-list'),
    path('sales/<int:pk>/', views.SaleDetailView.as_view(), name='sale-detail'),
    
    # Reports and Stats
    path('stats/', views.SalesStatsView.as_view(), name='sales-stats'),
    path('reports/', views.SaleReportListView.as_view(), name='report-list'),
    path('reports/generate/', views.GenerateReportView.as_view(), name='generate-report'),
]