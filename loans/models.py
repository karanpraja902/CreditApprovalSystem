from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer


class LoanProduct(models.Model):
    """Model for different loan products offered."""
    
    LOAN_TYPES = [
        ('PERSONAL', 'Personal Loan'),
        ('AUTO', 'Auto Loan'),
        ('MORTGAGE', 'Mortgage'),
        ('BUSINESS', 'Business Loan'),
        ('STUDENT', 'Student Loan'),
        ('CREDIT_CARD', 'Credit Card'),
    ]
    
    name = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=12, decimal_places=2)
    max_amount = models.DecimalField(max_digits=12, decimal_places=2)
    min_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    max_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    min_term_months = models.PositiveIntegerField()
    max_term_months = models.PositiveIntegerField()
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_products'
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.loan_type})"


class LoanApplication(models.Model):
    """Model for loan applications."""
    
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    EMPLOYMENT_TYPES = [
        ('FULL_TIME', 'Full Time'),
        ('PART_TIME', 'Part Time'),
        ('CONTRACT', 'Contract'),
        ('SELF_EMPLOYED', 'Self Employed'),
        ('UNEMPLOYED', 'Unemployed'),
        ('RETIRED', 'Retired'),
        ('STUDENT', 'Student'),
    ]
    
    # Application Details
    application_number = models.CharField(max_length=20, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='loan_applications')
    loan_product = models.ForeignKey(LoanProduct, on_delete=models.CASCADE)
    
    # Loan Details
    requested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    term_months = models.PositiveIntegerField()
    purpose = models.TextField()
    
    # Employment Information
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)
    employer_name = models.CharField(max_length=200, blank=True)
    job_title = models.CharField(max_length=200, blank=True)
    monthly_income = models.DecimalField(max_digits=10, decimal_places=2)
    years_at_current_job = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    
    # Financial Information
    monthly_expenses = models.DecimalField(max_digits=10, decimal_places=2)
    existing_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    assets_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Application Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    submitted_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    decision_notes = models.TextField(blank=True)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_applications'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.application_number} - {self.customer.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.application_number:
            # Generate application number
            import uuid
            self.application_number = f"LA{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)
    
    @property
    def debt_to_income_ratio(self):
        """Calculate debt-to-income ratio."""
        if self.monthly_income > 0:
            return (self.monthly_expenses + self.existing_debt) / self.monthly_income
        return 0
    
    @property
    def monthly_payment_estimate(self):
        """Calculate estimated monthly payment."""
        if self.approved_amount and self.interest_rate and self.term_months:
            principal = float(self.approved_amount)
            rate = float(self.interest_rate) / 100 / 12
            months = self.term_months
            
            if rate > 0:
                payment = principal * (rate * (1 + rate) ** months) / ((1 + rate) ** months - 1)
                return round(payment, 2)
            else:
                return round(principal / months, 2)
        return 0


class LoanDocument(models.Model):
    """Model for loan application documents."""
    
    DOCUMENT_TYPES = [
        ('INCOME_PROOF', 'Income Proof'),
        ('BANK_STATEMENT', 'Bank Statement'),
        ('EMPLOYMENT_LETTER', 'Employment Letter'),
        ('TAX_RETURN', 'Tax Return'),
        ('COLLATERAL_DOCS', 'Collateral Documents'),
        ('IDENTITY_PROOF', 'Identity Proof'),
        ('ADDRESS_PROOF', 'Address Proof'),
        ('OTHER', 'Other'),
    ]
    
    loan_application = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='loan_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'loan_documents'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.loan_application.application_number} - {self.document_type}"


class Loan(models.Model):
    """Model for approved and disbursed loans."""
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAID_OFF', 'Paid Off'),
        ('DEFAULTED', 'Defaulted'),
        ('CLOSED', 'Closed'),
    ]
    
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE)
    loan_number = models.CharField(max_length=20, unique=True)
    principal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    term_months = models.PositiveIntegerField()
    monthly_payment = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Loan Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    disbursed_at = models.DateTimeField()
    first_payment_date = models.DateField()
    maturity_date = models.DateField()
    
    # Current Balances
    outstanding_balance = models.DecimalField(max_digits=12, decimal_places=2)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.loan_number} - {self.loan_application.customer.full_name}"
    
    def save(self, *args, **kwargs):
        if not self.loan_number:
            # Generate loan number
            import uuid
            self.loan_number = f"LN{str(uuid.uuid4())[:8].upper()}"
        super().save(*args, **kwargs)