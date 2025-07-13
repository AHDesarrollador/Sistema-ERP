from rest_framework import serializers
from .models import Customer, Sale, SaleItem, SaleReport
from apps.inventory.models import Product, StockMovement

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'is_active', 'created_at']

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'product_sku', 'quantity', 
                 'unit_price', 'discount_amount', 'subtotal']
        read_only_fields = ['subtotal']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, required=False)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Sale
        fields = ['id', 'sale_number', 'customer', 'customer_name', 'user', 'user_name',
                 'subtotal', 'tax_amount', 'discount_amount', 'total_amount',
                 'payment_method', 'status', 'notes', 'items', 'created_at', 'updated_at']
        read_only_fields = ['sale_number', 'user']

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        validated_data['user'] = self.context['request'].user
        sale = Sale.objects.create(**validated_data)
        
        subtotal = 0
        for item_data in items_data:
            item = SaleItem.objects.create(sale=sale, **item_data)
            subtotal += item.subtotal
            
            # Update product stock
            product = item.product
            product.current_stock -= item.quantity
            product.save()
            
            # Create stock movement
            StockMovement.objects.create(
                product=product,
                movement_type='OUT',
                quantity=item.quantity,
                reference=f"Sale {sale.sale_number}",
                user=sale.user
            )
        
        # Update sale totals
        sale.subtotal = subtotal
        sale.total_amount = sale.subtotal + sale.tax_amount - sale.discount_amount
        sale.save()
        
        return sale

class SaleReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.username', read_only=True)
    
    class Meta:
        model = SaleReport
        fields = ['id', 'report_type', 'start_date', 'end_date', 'total_sales',
                 'total_transactions', 'average_sale_amount', 'generated_by',
                 'generated_by_name', 'generated_at']
        read_only_fields = ['generated_by']