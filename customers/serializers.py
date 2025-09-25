from rest_framework import serializers
from .models import Customer, CustomerDocument


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model."""
    
    full_name = serializers.ReadOnlyField()
    age = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email', 'phone_number',
            'date_of_birth', 'age', 'gender', 'marital_status', 'address_line_1',
            'address_line_2', 'city', 'state', 'postal_code', 'country',
            'annual_income', 'employment_status', 'employer_name', 'years_employed',
            'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CustomerCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating Customer."""
    
    class Meta:
        model = Customer
        fields = [
            'first_name', 'last_name', 'email', 'phone_number', 'date_of_birth',
            'gender', 'marital_status', 'address_line_1', 'address_line_2',
            'city', 'state', 'postal_code', 'country', 'annual_income',
            'employment_status', 'employer_name', 'years_employed'
        ]


class CustomerDocumentSerializer(serializers.ModelSerializer):
    """Serializer for CustomerDocument model."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    verified_by_name = serializers.CharField(source='verified_by.username', read_only=True)
    
    class Meta:
        model = CustomerDocument
        fields = [
            'id', 'customer', 'customer_name', 'document_type', 'document_name',
            'document_file', 'uploaded_at', 'is_verified', 'verified_at',
            'verified_by', 'verified_by_name'
        ]
        read_only_fields = ['id', 'uploaded_at', 'verified_at', 'verified_by']


class CustomerSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for customer summary."""
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = Customer
        fields = ['id', 'full_name', 'email', 'phone_number', 'annual_income', 'is_active']