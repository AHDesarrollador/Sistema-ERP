"""
API Root view for ERP Dashboard
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.http import HttpResponse
from django.template import Template, Context

@api_view(['GET'])
@permission_classes([AllowAny])
def api_root(request, format=None):
    """
    API Root - Navigate through available endpoints
    """
    return Response({
        'message': 'Welcome to ERP Dashboard API',
        'version': '1.0',
        'authentication': 'Token based authentication required for most endpoints',
        'endpoints': {
            'users': {
                'register': reverse('users:register', request=request, format=format),
                'login': reverse('users:login', request=request, format=format),
                'profile': reverse('users:profile', request=request, format=format),
                'list': reverse('users:user-list', request=request, format=format),
            },
            'inventory': {
                'products': reverse('inventory:product-list', request=request, format=format),
                'categories': reverse('inventory:category-list', request=request, format=format),
                'suppliers': reverse('inventory:supplier-list', request=request, format=format),
                'stock_movements': reverse('inventory:stock-movement-list', request=request, format=format),
                'stats': reverse('inventory:inventory-stats', request=request, format=format),
                'low_stock': reverse('inventory:low-stock-products', request=request, format=format),
            },
            'sales': {
                'sales': reverse('sales:sale-list', request=request, format=format),
                'customers': reverse('sales:customer-list', request=request, format=format),
                'stats': reverse('sales:sales-stats', request=request, format=format),
                'reports': reverse('sales:report-list', request=request, format=format),
                'generate_report': reverse('sales:generate-report', request=request, format=format),
            }
        },
        'documentation': {
            'admin_panel': request.build_absolute_uri('/admin/'),
            'dashboard': request.build_absolute_uri('/dashboard/'),
            'browsable_api': 'Add ?format=json to any endpoint for JSON response'
        },
        'sample_requests': {
            'get_inventory_stats': {
                'url': reverse('inventory:inventory-stats', request=request, format=format),
                'method': 'GET',
                'headers': {
                    'Authorization': 'Token YOUR_TOKEN_HERE'
                }
            },
            'get_sales_stats': {
                'url': reverse('sales:sales-stats', request=request, format=format),
                'method': 'GET',
                'headers': {
                    'Authorization': 'Token YOUR_TOKEN_HERE'
                }
            }
        }
    })

def api_docs_view(request):
    """
    HTML documentation for the API
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ERP Dashboard API Documentation</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .endpoint { margin-bottom: 20px; padding: 15px; border-left: 4px solid #007bff; background: #f8f9fa; }
            .method-get { border-left-color: #28a745; }
            .method-post { border-left-color: #ffc107; }
            .method-put { border-left-color: #17a2b8; }
            .method-delete { border-left-color: #dc3545; }
            pre { background: #f1f1f1; padding: 10px; border-radius: 5px; }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="#">🔗 ERP API Documentation</a>
                <div class="navbar-nav flex-row">
                    <a class="nav-link mx-2" href="/admin/">Admin</a>
                    <a class="nav-link mx-2" href="/dashboard/">Dashboard</a>
                    <a class="nav-link mx-2" href="/api/">API Root</a>
                </div>
            </div>
        </nav>

        <div class="container mt-4">
            <h1>🔗 ERP Dashboard API</h1>
            <p class="lead">RESTful API for managing inventory, sales, and user data</p>

            <div class="alert alert-info">
                <h5>🔑 Authentication Required</h5>
                <p>Most endpoints require token authentication. Include header:</p>
                <pre>Authorization: Token YOUR_TOKEN_HERE</pre>
                <p>Get your token from: <a href="/admin/" target="_blank">Admin Panel → Tokens</a></p>
            </div>

            <h2>👥 Users API</h2>
            <div class="endpoint method-post">
                <strong>POST /api/users/register/</strong> - Register new user
                <pre>{"username": "user", "email": "user@example.com", "password": "pass123", "password_confirm": "pass123"}</pre>
            </div>
            
            <div class="endpoint method-post">
                <strong>POST /api/users/login/</strong> - Login user
                <pre>{"email": "user@example.com", "password": "pass123"}</pre>
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/users/profile/</strong> - Get user profile (requires auth)
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/users/list/</strong> - List all users (requires auth)
            </div>

            <h2>📦 Inventory API</h2>
            <div class="endpoint method-get">
                <strong>GET /api/inventory/products/</strong> - List products
                <p>Supports filtering: ?category=1&supplier=1&is_active=true</p>
                <p>Supports search: ?search=laptop</p>
            </div>
            
            <div class="endpoint method-post">
                <strong>POST /api/inventory/products/</strong> - Create product
                <pre>{"name": "Product", "sku": "SKU123", "category": 1, "supplier": 1, "cost_price": "100.00", "selling_price": "150.00"}</pre>
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/inventory/categories/</strong> - List categories
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/inventory/suppliers/</strong> - List suppliers
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/inventory/stock-movements/</strong> - List stock movements
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/inventory/stats/</strong> - Get inventory statistics
                <pre>Response: {"total_products": 10, "total_stock_value": 5000.0, "low_stock_products": 2}</pre>
            </div>

            <h2>💰 Sales API</h2>
            <div class="endpoint method-get">
                <strong>GET /api/sales/sales/</strong> - List sales
                <p>Supports filtering: ?status=COMPLETED&payment_method=CASH</p>
            </div>
            
            <div class="endpoint method-post">
                <strong>POST /api/sales/sales/</strong> - Create sale
                <pre>{"customer": 1, "items": [{"product": 1, "quantity": 2, "unit_price": "100.00"}], "payment_method": "CASH"}</pre>
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/sales/customers/</strong> - List customers
            </div>
            
            <div class="endpoint method-get">
                <strong>GET /api/sales/stats/</strong> - Get sales statistics
                <pre>Response: {"today": {"total_amount": 500}, "week": {"total_amount": 2000}, "month": {"total_amount": 8000}}</pre>
            </div>
            
            <div class="endpoint method-post">
                <strong>POST /api/sales/reports/generate/</strong> - Generate sales report
                <pre>{"report_type": "MONTHLY", "start_date": "2023-01-01", "end_date": "2023-01-31"}</pre>
            </div>

            <h2>🧪 Testing Examples</h2>
            <div class="alert alert-secondary">
                <h5>Using curl:</h5>
                <pre>
# Get inventory stats
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/inventory/stats/

# Get sales stats  
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/sales/stats/

# List products
curl -H "Authorization: Token YOUR_TOKEN" http://localhost:8000/api/inventory/products/
                </pre>
            </div>

            <h2>🔗 Related Links</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5>👨‍💼 Admin Panel</h5>
                            <p>Manage data through web interface</p>
                            <a href="/admin/" class="btn btn-primary">Open Admin</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5>📊 Dashboard</h5>
                            <p>View real-time analytics</p>
                            <a href="/dashboard/" class="btn btn-success">Open Dashboard</a>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5>🔗 API Root</h5>
                            <p>Browsable API endpoints</p>
                            <a href="/api/?format=api" class="btn btn-info">Open API</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="bg-dark text-white mt-5 py-3">
            <div class="container text-center">
                <p>ERP Dashboard API - Version 1.0</p>
            </div>
        </footer>
    </body>
    </html>
    """
    
    return HttpResponse(html_template)