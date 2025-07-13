"""
Home page view for ERP Dashboard
"""
from django.http import HttpResponse

def home_view(request):
    """
    Home page with navigation to all sections
    """
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ERP Dashboard System</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .hero { color: white; text-align: center; padding: 100px 0; }
            .feature-card { margin-bottom: 30px; transition: transform 0.3s; }
            .feature-card:hover { transform: translateY(-5px); }
            .stats { background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-dark">
            <div class="container">
                <a class="navbar-brand" href="/">🏢 ERP Dashboard</a>
                <div class="navbar-nav ml-auto">
                    <a class="nav-link" href="/admin/">👨‍💼 Admin</a>
                    <a class="nav-link" href="/api/">🔗 API</a>
                    <a class="nav-link" href="/dashboard/">📊 Dashboard</a>
                </div>
            </div>
        </nav>

        <div class="hero">
            <div class="container">
                <h1 class="display-4 mb-4">🏢 ERP Dashboard System</h1>
                <p class="lead mb-5">Complete Enterprise Resource Planning solution with real-time analytics</p>
                
                <div class="row justify-content-center">
                    <div class="col-md-8">
                        <div class="stats rounded p-4 mb-5">
                            <div class="row text-center">
                                <div class="col-md-3">
                                    <h3>📦</h3>
                                    <h4>Inventory</h4>
                                    <p>Complete stock management</p>
                                </div>
                                <div class="col-md-3">
                                    <h3>💰</h3>
                                    <h4>Sales</h4>
                                    <p>Transaction processing</p>
                                </div>
                                <div class="col-md-3">
                                    <h3>📊</h3>
                                    <h4>Analytics</h4>
                                    <p>Real-time dashboards</p>
                                </div>
                                <div class="col-md-3">
                                    <h3>🔗</h3>
                                    <h4>API</h4>
                                    <p>RESTful endpoints</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="container py-5">
            <div class="row">
                <div class="col-md-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <h2 class="text-primary">👨‍💼</h2>
                            <h4>Admin Panel</h4>
                            <p>Manage all your business data through a powerful web interface. Create, edit, and monitor products, sales, users, and more.</p>
                            <a href="/admin/" class="btn btn-primary">Access Admin</a>
                            <hr>
                            <small class="text-muted">
                                <strong>Secure login required</strong><br>
                                Contact administrator for access
                            </small>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <h2 class="text-success">📊</h2>
                            <h4>Interactive Dashboard</h4>
                            <p>View real-time business metrics with interactive charts. Monitor sales performance, inventory levels, and key indicators.</p>
                            <a href="/dashboard/" class="btn btn-success">View Dashboard</a>
                            <hr>
                            <small class="text-muted">
                                <strong>Features:</strong><br>
                                • Real-time data<br>
                                • Interactive charts<br>
                                • Auto-refresh
                            </small>
                        </div>
                    </div>
                </div>

                <div class="col-md-4">
                    <div class="card feature-card h-100">
                        <div class="card-body text-center">
                            <h2 class="text-info">🔗</h2>
                            <h4>RESTful API</h4>
                            <p>Integrate with external systems using our comprehensive REST API. Full CRUD operations for all business entities.</p>
                            <a href="/api/" class="btn btn-info">Explore API</a>
                            <hr>
                            <small class="text-muted">
                                <strong>Endpoints:</strong><br>
                                • Inventory management<br>
                                • Sales processing<br>
                                • User authentication
                            </small>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-5">
                <div class="col-12 text-center">
                    <h3>🚀 Quick Start</h3>
                    <div class="alert alert-light">
                        <div class="row">
                            <div class="col-md-4">
                                <h5>1. Admin Panel</h5>
                                <p>Secure login required for system management</p>
                            </div>
                            <div class="col-md-4">
                                <h5>2. Dashboard</h5>
                                <p>Authentication and permissions required</p>
                            </div>
                            <div class="col-md-4">
                                <h5>3. API</h5>
                                <p>Token-based authentication for integration</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <footer class="bg-dark text-white py-4">
            <div class="container text-center">
                <h5>ERP Dashboard System</h5>
                <p>Complete business management solution with inventory, sales, and analytics</p>
                <div class="mt-3">
                    <a href="/admin/" class="btn btn-outline-light btn-sm mx-1">Admin</a>
                    <a href="/api/" class="btn btn-outline-light btn-sm mx-1">API</a>
                    <a href="/dashboard/" class="btn btn-outline-light btn-sm mx-1">Dashboard</a>
                    <a href="/api/docs/" class="btn btn-outline-light btn-sm mx-1">Docs</a>
                </div>
            </div>
        </footer>
    </body>
    </html>
    """
    
    return HttpResponse(html_template)