from rest_framework import serializers
from .models import LoanProduct, LoanApplication, LoanDocument, Loan
from customers.serializers import CustomerSummarySerializer


class LoanProductSerializer(serializers.ModelSerializer):
    """Serializer for LoanProduct model."""
    
    class Meta:
        model = LoanProduct
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class LoanDocumentSerializer(serializers.ModelSerializer):
    """Serializer for LoanDocument model."""
    
    verified_by_name = serializers.CharField(source='verified_by.username', read_only=True)
    
    class Meta:
        model = LoanDocument
        fields = [
            'id', 'loan_application', 'document_type', 'document_name',
            'document_file', 'uploaded_at', 'is_verified', 'verified_at',
            'verified_by', 'verified_by_name', 'notes'
        ]
        read_only_fields = ['id', 'uploaded_at', 'verified_at', 'verified_by']


class LoanApplicationSerializer(serializers.ModelSerializer):
    """Serializer for LoanApplication model."""
    
    customer_details = CustomerSummarySerializer(source='customer', read_only=True)
    loan_product_name = serializers.CharField(source='loan_product.name', read_only=True)
    debt_to_income_ratio = serializers.ReadOnlyField()
    monthly_payment_estimate = serializers.ReadOnlyField()
    reviewed_by_name = serializers.CharField(source='reviewed_by.username', read_only=True)
    documents = LoanDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = [
            'id', 'application_number', 'customer', 'customer_details',
            'loan_product', 'loan_product_name', 'requested_amount',
            'approved_amount', 'interest_rate', 'term_months', 'purpose',
            'employment_type', 'employer_name', 'job_title', 'monthly_income',
            'years_at_current_job', 'monthly_expenses', 'existing_debt',
            'assets_value', 'debt_to_income_ratio', 'monthly_payment_estimate',
            'status', 'submitted_at', 'reviewed_at', 'reviewed_by',
            'reviewed_by_name', 'decision_notes', 'documents',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'application_number', 'debt_to_income_ratio',
            'monthly_payment_estimate', 'reviewed_at', 'reviewed_by',
            'created_at', 'updated_at'
        ]


class LoanApplicationCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating LoanApplication."""
    
    class Meta:
        model = LoanApplication
        fields = [
            'customer', 'loan_product', 'requested_amount', 'term_months',
            'purpose', 'employment_type', 'employer_name', 'job_title',
            'monthly_income', 'years_at_current_job', 'monthly_expenses',
            'existing_debt', 'assets_value'
        ]


class LoanApplicationSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for loan application summary."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    loan_product_name = serializers.CharField(source='loan_product.name', read_only=True)
    
    class Meta:
        model = LoanApplication
        fields = [
            'id', 'application_number', 'customer_name', 'loan_product_name',
            'requested_amount', 'status', 'submitted_at', 'created_at'
        ]


class LoanSerializer(serializers.ModelSerializer):
    """Serializer for Loan model."""
    
    customer_name = serializers.CharField(source='loan_application.customer.full_name', read_only=True)
    application_number = serializers.CharField(source='loan_application.application_number', read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'id', 'loan_number', 'loan_application', 'application_number',
            'customer_name', 'principal_amount', 'interest_rate', 'term_months',
            'monthly_payment', 'status', 'disbursed_at', 'first_payment_date',
            'maturity_date', 'outstanding_balance', 'total_paid',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'loan_number', 'created_at', 'updated_at']


class LoanSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for loan summary."""
    
    customer_name = serializers.CharField(source='loan_application.customer.full_name', read_only=True)
    
    class Meta:
        model = Loan
        fields = [
            'id', 'loan_number', 'customer_name', 'principal_amount',
            'outstanding_balance', 'status', 'disbursed_at'
        ]