from rest_framework import serializers
from .models import CreditScore, CreditReport, RiskAssessment, ScoringModel, CreditDecision


class CreditScoreSerializer(serializers.ModelSerializer):
    """Serializer for CreditScore model."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    
    class Meta:
        model = CreditScore
        fields = [
            'id', 'customer', 'customer_name', 'score', 'source',
            'score_date', 'factors', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CreditReportSerializer(serializers.ModelSerializer):
    """Serializer for CreditReport model."""
    
    customer_name = serializers.CharField(source='customer.full_name', read_only=True)
    credit_utilization_ratio = serializers.ReadOnlyField()
    
    class Meta:
        model = CreditReport
        fields = [
            'id', 'customer', 'customer_name', 'report_type', 'report_data',
            'report_date', 'bureau_source', 'total_accounts', 'open_accounts',
            'total_balance', 'total_credit_limit', 'credit_utilization_ratio',
            'oldest_account_age_months', 'recent_inquiries', 'delinquent_accounts',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class RiskAssessmentSerializer(serializers.ModelSerializer):
    """Serializer for RiskAssessment model."""
    
    application_number = serializers.CharField(source='loan_application.application_number', read_only=True)
    customer_name = serializers.CharField(source='loan_application.customer.full_name', read_only=True)
    
    class Meta:
        model = RiskAssessment
        fields = [
            'id', 'loan_application', 'application_number', 'customer_name',
            'risk_score', 'risk_level', 'assessment_method', 'credit_score_factor',
            'income_factor', 'debt_to_income_factor', 'employment_factor',
            'collateral_factor', 'assessment_notes', 'recommended_action',
            'recommended_interest_rate', 'recommended_amount', 'assessed_at',
            'assessed_by'
        ]
        read_only_fields = ['id', 'assessed_at']


class RiskAssessmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating RiskAssessment."""
    
    class Meta:
        model = RiskAssessment
        fields = [
            'loan_application', 'risk_score', 'risk_level', 'assessment_method',
            'credit_score_factor', 'income_factor', 'debt_to_income_factor',
            'employment_factor', 'collateral_factor', 'assessment_notes',
            'recommended_action', 'recommended_interest_rate', 'recommended_amount',
            'assessed_by'
        ]


class ScoringModelSerializer(serializers.ModelSerializer):
    """Serializer for ScoringModel."""
    
    class Meta:
        model = ScoringModel
        fields = [
            'id', 'name', 'model_type', 'version', 'description', 'configuration',
            'accuracy', 'precision', 'recall', 'f1_score', 'is_active',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class CreditDecisionSerializer(serializers.ModelSerializer):
    """Serializer for CreditDecision model."""
    
    application_number = serializers.CharField(source='loan_application.application_number', read_only=True)
    customer_name = serializers.CharField(source='loan_application.customer.full_name', read_only=True)
    
    class Meta:
        model = CreditDecision
        fields = [
            'id', 'loan_application', 'application_number', 'customer_name',
            'decision', 'decision_date', 'approved_amount', 'approved_rate',
            'conditions', 'decision_reason', 'decided_by_system',
            'decided_by_user', 'is_override', 'override_reason'
        ]
        read_only_fields = ['id', 'decision_date']


class CreditDecisionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating CreditDecision."""
    
    class Meta:
        model = CreditDecision
        fields = [
            'loan_application', 'decision', 'approved_amount', 'approved_rate',
            'conditions', 'decision_reason', 'decided_by_system',
            'decided_by_user', 'is_override', 'override_reason'
        ]


class CreditSummarySerializer(serializers.Serializer):
    """Serializer for credit summary information."""
    
    customer_id = serializers.IntegerField()
    customer_name = serializers.CharField()
    latest_credit_score = serializers.IntegerField(allow_null=True)
    credit_score_source = serializers.CharField(allow_null=True)
    total_applications = serializers.IntegerField()
    approved_applications = serializers.IntegerField()
    total_approved_amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_risk_score = serializers.DecimalField(max_digits=5, decimal_places=2, allow_null=True)