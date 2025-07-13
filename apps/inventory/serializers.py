from rest_framework import serializers
from .models import Category, Supplier, Product, StockMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'created_at']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'email', 'phone', 
                 'address', 'is_active', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_low_stock = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'barcode', 'description', 'category', 
                 'category_name', 'supplier', 'supplier_name', 'cost_price', 
                 'selling_price', 'current_stock', 'minimum_stock', 
                 'maximum_stock', 'unit', 'is_active', 'is_low_stock',
                 'created_at', 'updated_at']

class StockMovementSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'product_name', 'movement_type', 
                 'quantity', 'reference', 'notes', 'user', 'user_name', 
                 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        stock_movement = super().create(validated_data)
        
        product = stock_movement.product
        if stock_movement.movement_type == 'IN':
            product.current_stock += stock_movement.quantity
        elif stock_movement.movement_type == 'OUT':
            product.current_stock -= stock_movement.quantity
        elif stock_movement.movement_type == 'ADJUSTMENT':
            product.current_stock = stock_movement.quantity
        
        product.save()
        return stock_movement