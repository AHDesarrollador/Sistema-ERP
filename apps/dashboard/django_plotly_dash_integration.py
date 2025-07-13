from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .dash_app import dash_app

@login_required
def dashboard_view(request):
    """Django view to serve the Dash app"""
    return render(request, 'dashboard/dashboard.html', {
        'dash_app_url': '/dashboard/app/'
    })

def dash_app_view(request):
    """Serve the Dash app"""
    return HttpResponse(dash_app.index())