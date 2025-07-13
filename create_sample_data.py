#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp_dashboard_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.inventory.models import Category, Supplier, Product, StockMovement
from apps.sales.models import Customer, Sale, SaleItem
from decimal import Decimal

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create admin user token
    from rest_framework.authtoken.models import Token
    admin_user = User.objects.get(username='admin')
    token, created = Token.objects.get_or_create(user=admin_user)
    print(f"Admin token: {token.key}")
    
    # Create categories
    categories = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Clothing', 'description': 'Apparel and fashion items'},
        {'name': 'Books', 'description': 'Books and publications'},
        {'name': 'Food', 'description': 'Food and beverages'},
    ]
    
    for cat_data in categories:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created category: {category.name}")
    
    # Create suppliers
    suppliers = [
        {'name': 'TechSupply Inc', 'contact_person': 'John Smith', 'email': 'john@techsupply.com', 'phone': '555-0101'},
        {'name': 'Fashion World', 'contact_person': 'Jane Doe', 'email': 'jane@fashionworld.com', 'phone': '555-0102'},
        {'name': 'Book Publishers', 'contact_person': 'Bob Wilson', 'email': 'bob@bookpub.com', 'phone': '555-0103'},
        {'name': 'Food Distributors', 'contact_person': 'Alice Brown', 'email': 'alice@fooddist.com', 'phone': '555-0104'},
    ]
    
    for sup_data in suppliers:
        supplier, created = Supplier.objects.get_or_create(
            name=sup_data['name'],
            defaults=sup_data
        )
        if created:
            print(f"Created supplier: {supplier.name}")
    
    # Create products
    products = [
        {'name': 'Laptop Dell XPS 13', 'sku': 'DELL-XPS13', 'category': 'Electronics', 'supplier': 'TechSupply Inc', 'cost_price': 800, 'selling_price': 1200, 'current_stock': 15, 'minimum_stock': 5},
        {'name': 'iPhone 15', 'sku': 'IPHONE-15', 'category': 'Electronics', 'supplier': 'TechSupply Inc', 'cost_price': 700, 'selling_price': 1000, 'current_stock': 8, 'minimum_stock': 10},
        {'name': 'T-Shirt Blue', 'sku': 'TSHIRT-BLU', 'category': 'Clothing', 'supplier': 'Fashion World', 'cost_price': 10, 'selling_price': 25, 'current_stock': 50, 'minimum_stock': 20},
        {'name': 'Jeans Classic', 'sku': 'JEANS-CLS', 'category': 'Clothing', 'supplier': 'Fashion World', 'cost_price': 25, 'selling_price': 60, 'current_stock': 30, 'minimum_stock': 15},
        {'name': 'Python Programming Book', 'sku': 'BOOK-PYTHON', 'category': 'Books', 'supplier': 'Book Publishers', 'cost_price': 20, 'selling_price': 45, 'current_stock': 25, 'minimum_stock': 10},
        {'name': 'Coffee Premium', 'sku': 'COFFEE-PREM', 'category': 'Food', 'supplier': 'Food Distributors', 'cost_price': 8, 'selling_price': 15, 'current_stock': 3, 'minimum_stock': 20},
    ]
    
    for prod_data in products:
        category = Category.objects.get(name=prod_data['category'])
        supplier = Supplier.objects.get(name=prod_data['supplier'])
        
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults={
                'name': prod_data['name'],
                'category': category,
                'supplier': supplier,
                'cost_price': Decimal(str(prod_data['cost_price'])),
                'selling_price': Decimal(str(prod_data['selling_price'])),
                'current_stock': prod_data['current_stock'],
                'minimum_stock': prod_data['minimum_stock'],
            }
        )
        if created:
            print(f"Created product: {product.name}")
    
    # Create customers
    customers = [
        {'name': 'Maria Garcia', 'email': 'maria@email.com', 'phone': '555-1001'},
        {'name': 'Carlos Rodriguez', 'email': 'carlos@email.com', 'phone': '555-1002'},
        {'name': 'Ana Martinez', 'email': 'ana@email.com', 'phone': '555-1003'},
        {'name': 'Luis Fernandez', 'email': 'luis@email.com', 'phone': '555-1004'},
    ]
    
    for cust_data in customers:
        customer, created = Customer.objects.get_or_create(
            email=cust_data['email'],
            defaults=cust_data
        )
        if created:
            print(f"Created customer: {customer.name}")
    
    # Create some sales
    customers_list = list(Customer.objects.all())
    products_list = list(Product.objects.all())
    
    for i in range(5):
        sale = Sale.objects.create(
            customer=customers_list[i % len(customers_list)],
            user=admin_user,
            status='COMPLETED',
            payment_method='CASH'
        )
        
        # Add items to sale
        total = Decimal('0')
        for j in range(2):  # 2 items per sale
            product = products_list[j % len(products_list)]
            quantity = 2
            unit_price = product.selling_price
            
            item = SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                unit_price=unit_price,
                subtotal=quantity * unit_price
            )
            total += item.subtotal
            
            # Update stock
            product.current_stock -= quantity
            product.save()
            
            # Create stock movement
            StockMovement.objects.create(
                product=product,
                movement_type='OUT',
                quantity=quantity,
                reference=f"Sale {sale.sale_number}",
                user=admin_user
            )
        
        sale.subtotal = total
        sale.total_amount = total
        sale.save()
        print(f"Created sale: {sale.sale_number}")
    
    print("\nSample data created successfully!")
    print(f"Admin username: admin")
    print(f"Admin password: admin123")
    print(f"API Token: {token.key}")
    print("\nURLs to test:")
    print("- Admin: http://localhost:8001/admin/")
    print("- API: http://localhost:8001/api/")
    print("- Dashboard: http://localhost:8001/dashboard/")

if __name__ == '__main__':
    create_sample_data()