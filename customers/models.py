from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Customer(models.Model):
    """Customer model for storing customer information."""
    
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    ]
    
    # Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES)
    
    # Address Information
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='USA')
    
    # Financial Information
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    employment_status = models.CharField(max_length=100)
    employer_name = models.CharField(max_length=200, blank=True)
    years_employed = models.PositiveIntegerField(default=0)
    
    # System Fields
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'customers'
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.date_of_birth.year - (
            (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
        )


class CustomerDocument(models.Model):
    """Model for storing customer documents."""
    
    DOCUMENT_TYPES = [
        ('ID', 'Government ID'),
        ('PASSPORT', 'Passport'),
        ('DRIVER_LICENSE', 'Driver License'),
        ('UTILITY_BILL', 'Utility Bill'),
        ('BANK_STATEMENT', 'Bank Statement'),
        ('PAY_STUB', 'Pay Stub'),
        ('TAX_RETURN', 'Tax Return'),
        ('OTHER', 'Other'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_name = models.CharField(max_length=255)
    document_file = models.FileField(upload_to='customer_documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        db_table = 'customer_documents'
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.document_type}"