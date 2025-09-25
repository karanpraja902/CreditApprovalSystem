from django.contrib import admin
from .models import CreditScore, CreditReport, RiskAssessment, ScoringModel, CreditDecision


@admin.register(CreditScore)
class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ['customer', 'score', 'source', 'score_date', 'created_at']
    list_filter = ['source', 'score_date', 'created_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'customer__email']
    readonly_fields = ['created_at']
    date_hierarchy = 'score_date'


@admin.register(CreditReport)
class CreditReportAdmin(admin.ModelAdmin):
    list_display = ['customer', 'report_type', 'bureau_source', 'total_accounts', 'total_balance', 'report_date']
    list_filter = ['report_type', 'bureau_source', 'report_date']
    search_fields = ['customer__first_name', 'customer__last_name']
    readonly_fields = ['created_at', 'credit_utilization_ratio']
    date_hierarchy = 'report_date'


@admin.register(RiskAssessment)
class RiskAssessmentAdmin(admin.ModelAdmin):
    list_display = ['loan_application', 'risk_score', 'risk_level', 'recommended_action', 'assessed_at']
    list_filter = ['risk_level', 'assessment_method', 'recommended_action', 'assessed_at']
    search_fields = ['loan_application__application_number', 'loan_application__customer__first_name']
    readonly_fields = ['assessed_at']
    
    fieldsets = (
        ('Assessment Overview', {
            'fields': ('loan_application', 'risk_score', 'risk_level', 'assessment_method')
        }),
        ('Risk Factors', {
            'fields': ('credit_score_factor', 'income_factor', 'debt_to_income_factor', 
                      'employment_factor', 'collateral_factor')
        }),
        ('Recommendations', {
            'fields': ('recommended_action', 'recommended_interest_rate', 'recommended_amount')
        }),
        ('Assessment Details', {
            'fields': ('assessment_notes', 'assessed_at', 'assessed_by')
        }),
    )


@admin.register(ScoringModel)
class ScoringModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_type', 'version', 'accuracy', 'is_active', 'created_at']
    list_filter = ['model_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(CreditDecision)
class CreditDecisionAdmin(admin.ModelAdmin):
    list_display = ['loan_application', 'decision', 'approved_amount', 'approved_rate', 'decision_date']
    list_filter = ['decision', 'decided_by_system', 'is_override', 'decision_date']
    search_fields = ['loan_application__application_number', 'loan_application__customer__first_name']
    readonly_fields = ['decision_date']