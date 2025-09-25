from django.contrib import admin
from .models import Customer, CustomerDocument


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'annual_income', 'employment_status', 'is_active', 'created_at']
    list_filter = ['gender', 'marital_status', 'employment_status', 'is_active', 'created_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at', 'age']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'age', 'gender', 'marital_status')
        }),
        ('Address Information', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Financial Information', {
            'fields': ('annual_income', 'employment_status', 'employer_name', 'years_employed')
        }),
        ('System Information', {
            'fields': ('user', 'is_active', 'created_at', 'updated_at')
        }),
    )


@admin.register(CustomerDocument)
class CustomerDocumentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'document_type', 'document_name', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified', 'uploaded_at']
    search_fields = ['customer__first_name', 'customer__last_name', 'document_name']
    readonly_fields = ['uploaded_at']