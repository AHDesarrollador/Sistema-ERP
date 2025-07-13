import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta
import requests
import json

# Initialize the Dash app
dash_app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

def get_api_data(endpoint, token):
    """Helper function to fetch data from Django API"""
    headers = {'Authorization': f'Token {token}'}
    try:
        response = requests.get(f'http://localhost:8000/api/{endpoint}', headers=headers)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {}

# Layout
dash_app.layout = html.Div([
    dcc.Store(id='auth-token'),
    html.Div([
        html.H1("ERP Dashboard", className="text-center mb-4"),
        
        # Auth section
        html.Div(id='auth-section', children=[
            html.Div([
                html.H3("Login Required"),
                dcc.Input(id='token-input', type='text', placeholder='Enter your API token'),
                html.Button('Login', id='login-btn', className='btn btn-primary ml-2')
            ], className='text-center')
        ]),
        
        # Main dashboard (hidden until authenticated)
        html.Div(id='dashboard-content', style={'display': 'none'}, children=[
            # Summary Cards
            html.Div(id='summary-cards', className='row mb-4'),
            
            # Charts Section
            html.Div([
                html.Div([
                    html.H4("Sales Overview"),
                    dcc.Graph(id='sales-chart')
                ], className='col-md-6'),
                
                html.Div([
                    html.H4("Inventory Status"),
                    dcc.Graph(id='inventory-chart')
                ], className='col-md-6'),
            ], className='row mb-4'),
            
            # Product Performance
            html.Div([
                html.H4("Top Products by Sales"),
                dcc.Graph(id='top-products-chart')
            ], className='row mb-4'),
            
            # Refresh button
            html.Div([
                html.Button('Refresh Data', id='refresh-btn', className='btn btn-success')
            ], className='text-center')
        ])
    ], className='container-fluid p-4')
])

@callback(
    [Output('auth-token', 'data'),
     Output('auth-section', 'style'),
     Output('dashboard-content', 'style')],
    [Input('login-btn', 'n_clicks')],
    [dash.dependencies.State('token-input', 'value')]
)
def handle_login(n_clicks, token):
    if n_clicks and token:
        # Validate token by making a test API call
        headers = {'Authorization': f'Token {token}'}
        try:
            response = requests.get('http://localhost:8000/api/users/profile/', headers=headers)
            if response.status_code == 200:
                return token, {'display': 'none'}, {'display': 'block'}
        except:
            pass
    
    return None, {'display': 'block'}, {'display': 'none'}

@callback(
    Output('summary-cards', 'children'),
    [Input('refresh-btn', 'n_clicks'),
     Input('auth-token', 'data')]
)
def update_summary_cards(n_clicks, token):
    if not token:
        return []
    
    # Fetch stats from APIs
    inventory_stats = get_api_data('inventory/stats/', token)
    sales_stats = get_api_data('sales/stats/', token)
    
    cards = [
        html.Div([
            html.Div([
                html.H5("Total Products", className="card-title"),
                html.H2(inventory_stats.get('total_products', 0), className="text-primary")
            ], className="card-body")
        ], className="card col-md-3"),
        
        html.Div([
            html.Div([
                html.H5("Stock Value", className="card-title"),
                html.H2(f"${inventory_stats.get('total_stock_value', 0):,.2f}", className="text-success")
            ], className="card-body")
        ], className="card col-md-3"),
        
        html.Div([
            html.Div([
                html.H5("Low Stock Items", className="card-title"),
                html.H2(inventory_stats.get('low_stock_products', 0), className="text-warning")
            ], className="card-body")
        ], className="card col-md-3"),
        
        html.Div([
            html.Div([
                html.H5("Today's Sales", className="card-title"),
                html.H2(f"${sales_stats.get('today', {}).get('total_amount', 0):,.2f}", className="text-info")
            ], className="card-body")
        ], className="card col-md-3"),
    ]
    
    return cards

@callback(
    Output('sales-chart', 'figure'),
    [Input('refresh-btn', 'n_clicks'),
     Input('auth-token', 'data')]
)
def update_sales_chart(n_clicks, token):
    if not token:
        return {}
    
    sales_stats = get_api_data('sales/stats/', token)
    
    # Create sample data for the chart
    data = {
        'Period': ['Today', 'This Week', 'This Month'],
        'Sales': [
            sales_stats.get('today', {}).get('total_amount', 0),
            sales_stats.get('week', {}).get('total_amount', 0),
            sales_stats.get('month', {}).get('total_amount', 0)
        ]
    }
    
    fig = px.bar(data, x='Period', y='Sales', title='Sales Performance')
    fig.update_layout(showlegend=False)
    return fig

@callback(
    Output('inventory-chart', 'figure'),
    [Input('refresh-btn', 'n_clicks'),
     Input('auth-token', 'data')]
)
def update_inventory_chart(n_clicks, token):
    if not token:
        return {}
    
    inventory_stats = get_api_data('inventory/stats/', token)
    
    # Create pie chart for inventory status
    data = {
        'Status': ['Normal Stock', 'Low Stock'],
        'Count': [
            inventory_stats.get('total_products', 0) - inventory_stats.get('low_stock_products', 0),
            inventory_stats.get('low_stock_products', 0)
        ]
    }
    
    fig = px.pie(data, values='Count', names='Status', title='Inventory Status Distribution')
    return fig

@callback(
    Output('top-products-chart', 'figure'),
    [Input('refresh-btn', 'n_clicks'),
     Input('auth-token', 'data')]
)
def update_top_products_chart(n_clicks, token):
    if not token:
        return {}
    
    # This would require additional API endpoint for top products
    # For now, creating sample data
    sample_data = {
        'Product': ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
        'Sales': [1200, 950, 800, 650, 500]
    }
    
    fig = px.bar(sample_data, x='Product', y='Sales', title='Top 5 Products by Sales')
    fig.update_layout(showlegend=False)
    return fig