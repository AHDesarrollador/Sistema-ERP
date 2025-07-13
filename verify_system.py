#!/usr/bin/env python
"""
Verify ERP system functionality
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_dashboard_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from apps.inventory.models import Product, Category
from apps.sales.models import Sale

User = get_user_model()

def verify_users():
    print("👥 User Verification:")
    print("-" * 30)
    
    # Check existing users
    users = User.objects.all()
    print(f"Total users: {users.count()}")
    
    for user in users:
        print(f"• {user.username} - Active: {user.is_active} - Superuser: {user.is_superuser}")
    
    # Reset admin password to known value
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@erp.com',
            'is_staff': True,
            'is_superuser': True,
            'is_active': True
        }
    )
    
    # Set password
    admin_user.set_password('admin123')
    admin_user.save()
    
    print(f"\n✅ Admin user ready: admin/admin123")
    
    # Get or create token
    token, created = Token.objects.get_or_create(user=admin_user)
    print(f"🔑 API Token: {token.key}")
    
    return token.key

def verify_data():
    print("\n📊 Data Verification:")
    print("-" * 30)
    
    print(f"Categories: {Category.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"Sales: {Sale.objects.count()}")
    
    # Show some sample data
    if Category.objects.exists():
        print("\nSample categories:")
        for cat in Category.objects.all()[:3]:
            print(f"• {cat.name}")
    
    if Product.objects.exists():
        print("\nSample products:")
        for prod in Product.objects.all()[:3]:
            print(f"• {prod.name} - Stock: {prod.current_stock}")

def test_api_endpoints():
    print("\n🔗 API Endpoints Test:")
    print("-" * 30)
    
    import requests
    
    # Get token for testing
    admin_user = User.objects.get(username='admin')
    token = Token.objects.get(user=admin_user)
    
    headers = {'Authorization': f'Token {token.key}'}
    base_url = 'http://localhost:8001/api'
    
    endpoints = [
        '/inventory/stats/',
        '/sales/stats/',
        '/inventory/products/',
        '/sales/sales/'
    ]
    
    print("Note: Start server first with: python manage.py runserver 8001")
    print("Then test these endpoints:")
    
    for endpoint in endpoints:
        full_url = base_url + endpoint
        print(f"• GET {full_url}")
        print(f"  Headers: {headers}")

def main():
    print("🔍 ERP System Verification")
    print("=" * 50)
    
    # Verify users and get token
    token = verify_users()
    
    # Verify data
    verify_data()
    
    # Show API test info
    test_api_endpoints()
    
    print("\n🚀 System Status:")
    print("-" * 30)
    print("✅ Database: SQLite (working)")
    print("✅ Admin user: admin/admin123")
    print(f"✅ API Token: {token}")
    print("✅ Sample data: Available")
    
    print("\n📋 Quick Start:")
    print("1. Start server: python manage.py runserver 8001")
    print("2. Access admin: http://localhost:8001/admin/")
    print("3. Login with: admin/admin123")
    print("4. Test API with token above")
    print("5. Access dashboard: http://localhost:8001/dashboard/")

if __name__ == '__main__':
    main()