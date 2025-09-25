from django.contrib import admin
from .models import LoanProduct, LoanApplication, LoanDocument, Loan


@admin.register(LoanProduct)
class LoanProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'loan_type', 'min_amount', 'max_amount', 'min_interest_rate', 'max_interest_rate', 'is_active']
    list_filter = ['loan_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ['application_number', 'customer', 'loan_product', 'requested_amount', 'status', 'submitted_at']
    list_filter = ['status', 'loan_product', 'employment_type', 'submitted_at']
    search_fields = ['application_number', 'customer__first_name', 'customer__last_name', 'customer__email']
    readonly_fields = ['application_number', 'created_at', 'updated_at', 'debt_to_income_ratio', 'monthly_payment_estimate']
    
    fieldsets = (
        ('Application Details', {
            'fields': ('application_number', 'customer', 'loan_product', 'status')
        }),
        ('Loan Details', {
            'fields': ('requested_amount', 'approved_amount', 'interest_rate', 'term_months', 'purpose')
        }),
        ('Employment Information', {
            'fields': ('employment_type', 'employer_name', 'job_title', 'monthly_income', 'years_at_current_job')
        }),
        ('Financial Information', {
            'fields': ('monthly_expenses', 'existing_debt', 'assets_value', 'debt_to_income_ratio', 'monthly_payment_estimate')
        }),
        ('Review Information', {
            'fields': ('submitted_at', 'reviewed_at', 'reviewed_by', 'decision_notes')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(LoanDocument)
class LoanDocumentAdmin(admin.ModelAdmin):
    list_display = ['loan_application', 'document_type', 'document_name', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['loan_application__application_number', 'document_name']
    readonly_fields = ['uploaded_at']


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['loan_number', 'loan_application', 'principal_amount', 'outstanding_balance', 'status', 'disbursed_at']
    list_filter = ['status', 'disbursed_at']
    search_fields = ['loan_number', 'loan_application__application_number', 'loan_application__customer__first_name']
    readonly_fields = ['loan_number', 'created_at', 'updated_at']