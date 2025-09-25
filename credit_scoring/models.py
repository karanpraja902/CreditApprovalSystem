from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from customers.models import Customer
from loans.models import LoanApplication


class CreditScore(models.Model):
    """Model for storing credit scores."""
    
    SCORE_SOURCES = [
        ('INTERNAL', 'Internal Calculation'),
        ('EXPERIAN', 'Experian'),
        ('EQUIFAX', 'Equifax'),
        ('TRANSUNION', 'TransUnion'),
        ('FICO', 'FICO'),
        ('VANTAGE', 'VantageScore'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='credit_scores')
    score = models.PositiveIntegerField(
        validators=[MinValueValidator(300), MaxValueValidator(850)]
    )
    source = models.CharField(max_length=20, choices=SCORE_SOURCES)
    score_date = models.DateTimeField()
    factors = models.JSONField(default=dict, blank=True)  # Store contributing factors
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'credit_scores'
        ordering = ['-score_date']
        unique_together = ['customer', 'source', 'score_date']
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.score} ({self.source})"


class CreditReport(models.Model):
    """Model for storing credit reports."""
    
    REPORT_TYPES = [
        ('FULL', 'Full Credit Report'),
        ('SUMMARY', 'Credit Summary'),
        ('MONITORING', 'Credit Monitoring'),
    ]
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='credit_reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    report_data = models.JSONField()  # Store the full report data
    report_date = models.DateTimeField()
    bureau_source = models.CharField(max_length=50)
    
    # Key metrics extracted from report
    total_accounts = models.PositiveIntegerField(default=0)
    open_accounts = models.PositiveIntegerField(default=0)
    total_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_credit_limit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    oldest_account_age_months = models.PositiveIntegerField(default=0)
    recent_inquiries = models.PositiveIntegerField(default=0)
    delinquent_accounts = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'credit_reports'
        ordering = ['-report_date']
        
    def __str__(self):
        return f"{self.customer.full_name} - {self.report_type} ({self.report_date.date()})"
    
    @property
    def credit_utilization_ratio(self):
        """Calculate credit utilization ratio."""
        if self.total_credit_limit > 0:
            return (self.total_balance / self.total_credit_limit) * 100
        return 0


class RiskAssessment(models.Model):
    """Model for risk assessment of loan applications."""
    
    RISK_LEVELS = [
        ('LOW', 'Low Risk'),
        ('MEDIUM', 'Medium Risk'),
        ('HIGH', 'High Risk'),
        ('VERY_HIGH', 'Very High Risk'),
    ]
    
    ASSESSMENT_METHODS = [
        ('AUTOMATED', 'Automated Scoring'),
        ('MANUAL', 'Manual Review'),
        ('HYBRID', 'Hybrid Assessment'),
    ]
    
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='risk_assessment')
    risk_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-100 scale
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    assessment_method = models.CharField(max_length=20, choices=ASSESSMENT_METHODS)
    
    # Risk factors
    credit_score_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    income_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    debt_to_income_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    employment_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    collateral_factor = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Assessment details
    assessment_notes = models.TextField(blank=True)
    recommended_action = models.CharField(max_length=20, choices=[
        ('APPROVE', 'Approve'),
        ('REJECT', 'Reject'),
        ('REVIEW', 'Manual Review Required'),
    ])
    recommended_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recommended_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    
    assessed_at = models.DateTimeField(auto_now_add=True)
    assessed_by = models.CharField(max_length=100, default='SYSTEM')  # System or user name
    
    class Meta:
        db_table = 'risk_assessments'
        ordering = ['-assessed_at']
        
    def __str__(self):
        return f"{self.loan_application.application_number} - {self.risk_level} ({self.risk_score})"


class ScoringModel(models.Model):
    """Model for storing different scoring models and their configurations."""
    
    MODEL_TYPES = [
        ('FICO', 'FICO Score Model'),
        ('VANTAGE', 'VantageScore Model'),
        ('CUSTOM', 'Custom Internal Model'),
        ('ML', 'Machine Learning Model'),
    ]
    
    name = models.CharField(max_length=100)
    model_type = models.CharField(max_length=20, choices=MODEL_TYPES)
    version = models.CharField(max_length=20)
    description = models.TextField()
    
    # Model configuration
    configuration = models.JSONField()  # Store model parameters and weights
    
    # Model performance metrics
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    precision = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recall = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    f1_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'scoring_models'
        ordering = ['-created_at']
        unique_together = ['name', 'version']
        
    def __str__(self):
        return f"{self.name} v{self.version}"


class CreditDecision(models.Model):
    """Model for storing final credit decisions."""
    
    DECISION_TYPES = [
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('CONDITIONAL', 'Conditional Approval'),
        ('DEFERRED', 'Deferred'),
    ]
    
    loan_application = models.OneToOneField(LoanApplication, on_delete=models.CASCADE, related_name='credit_decision')
    decision = models.CharField(max_length=20, choices=DECISION_TYPES)
    decision_date = models.DateTimeField(auto_now_add=True)
    
    # Decision details
    approved_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    approved_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    conditions = models.TextField(blank=True)
    decision_reason = models.TextField()
    
    # Decision maker
    decided_by_system = models.BooleanField(default=True)
    decided_by_user = models.CharField(max_length=100, blank=True)
    
    # Override information
    is_override = models.BooleanField(default=False)
    override_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'credit_decisions'
        ordering = ['-decision_date']
        
    def __str__(self):
        return f"{self.loan_application.application_number} - {self.decision}"