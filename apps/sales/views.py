from rest_framework import generics, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Customer, Sale, SaleItem, SaleReport
from .serializers import CustomerSerializer, SaleSerializer, SaleReportSerializer

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'phone']

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class SaleListCreateView(generics.ListCreateAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'payment_method', 'customer']
    ordering = ['-created_at']

class SaleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

class SalesStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Today's sales
        today_sales = Sale.objects.filter(
            created_at__date=today,
            status='COMPLETED'
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        
        # This week's sales
        week_sales = Sale.objects.filter(
            created_at__date__gte=week_ago,
            status='COMPLETED'
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id')
        )
        
        # This month's sales
        month_sales = Sale.objects.filter(
            created_at__date__gte=month_ago,
            status='COMPLETED'
        ).aggregate(
            total=Sum('total_amount'),
            count=Count('id'),
            avg=Avg('total_amount')
        )
        
        return Response({
            'today': {
                'total_amount': today_sales['total'] or 0,
                'total_transactions': today_sales['count'] or 0
            },
            'week': {
                'total_amount': week_sales['total'] or 0,
                'total_transactions': week_sales['count'] or 0
            },
            'month': {
                'total_amount': month_sales['total'] or 0,
                'total_transactions': month_sales['count'] or 0,
                'average_sale': month_sales['avg'] or 0
            }
        })

class GenerateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        report_type = request.data.get('report_type', 'DAILY')
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        
        if not start_date or not end_date:
            return Response(
                {'error': 'start_date and end_date are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Convert string dates to date objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Calculate report data
        sales = Sale.objects.filter(
            created_at__date__range=[start_date, end_date],
            status='COMPLETED'
        )
        
        report_data = sales.aggregate(
            total_sales=Sum('total_amount'),
            total_transactions=Count('id'),
            average_sale_amount=Avg('total_amount')
        )
        
        # Create report
        report = SaleReport.objects.create(
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            total_sales=report_data['total_sales'] or 0,
            total_transactions=report_data['total_transactions'] or 0,
            average_sale_amount=report_data['average_sale_amount'] or 0,
            generated_by=request.user
        )
        
        serializer = SaleReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SaleReportListView(generics.ListAPIView):
    queryset = SaleReport.objects.all()
    serializer_class = SaleReportSerializer
    permission_classes = [IsAuthenticated]
    ordering = ['-generated_at']
