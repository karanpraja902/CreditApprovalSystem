from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import LoanProduct, LoanApplication, LoanDocument, Loan
from .serializers import (
    LoanProductSerializer, LoanApplicationSerializer,
    LoanApplicationCreateSerializer, LoanApplicationSummarySerializer,
    LoanDocumentSerializer, LoanSerializer, LoanSummarySerializer
)


class LoanProductViewSet(viewsets.ModelViewSet):
    """ViewSet for managing loan products."""
    
    queryset = LoanProduct.objects.filter(is_active=True)
    serializer_class = LoanProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['loan_type', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'min_amount', 'max_amount']
    ordering = ['name']


class LoanApplicationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing loan applications."""
    
    queryset = LoanApplication.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'loan_product', 'employment_type', 'customer']
    search_fields = ['application_number', 'customer__first_name', 'customer__last_name']
    ordering_fields = ['created_at', 'submitted_at', 'requested_amount']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return LoanApplicationCreateSerializer
        elif self.action == 'list':
            return LoanApplicationSummarySerializer
        return LoanApplicationSerializer
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a loan application for review."""
        application = self.get_object()
        
        if application.status != 'DRAFT':
            return Response(
                {'error': 'Only draft applications can be submitted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'SUBMITTED'
        application.submitted_at = timezone.now()
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve a loan application."""
        application = self.get_object()
        
        if application.status not in ['SUBMITTED', 'UNDER_REVIEW']:
            return Response(
                {'error': 'Only submitted or under review applications can be approved'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        approved_amount = request.data.get('approved_amount')
        interest_rate = request.data.get('interest_rate')
        decision_notes = request.data.get('decision_notes', '')
        
        if not approved_amount or not interest_rate:
            return Response(
                {'error': 'approved_amount and interest_rate are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = 'APPROVED'
        application.approved_amount = approved_amount
        application.interest_rate = interest_rate
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.decision_notes = decision_notes
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """Reject a loan application."""
        application = self.get_object()
        
        if application.status not in ['SUBMITTED', 'UNDER_REVIEW']:
            return Response(
                {'error': 'Only submitted or under review applications can be rejected'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        decision_notes = request.data.get('decision_notes', '')
        
        application.status = 'REJECTED'
        application.reviewed_at = timezone.now()
        application.reviewed_by = request.user
        application.decision_notes = decision_notes
        application.save()
        
        serializer = self.get_serializer(application)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get all documents for a loan application."""
        application = self.get_object()
        documents = LoanDocument.objects.filter(loan_application=application)
        serializer = LoanDocumentSerializer(documents, many=True)
        return Response(serializer.data)


class LoanDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing loan documents."""
    
    queryset = LoanDocument.objects.all()
    serializer_class = LoanDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['loan_application', 'document_type', 'is_verified']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    @action(detail=True, methods=['patch'])
    def verify(self, request, pk=None):
        """Verify a loan document."""
        document = self.get_object()
        document.is_verified = True
        document.verified_by = request.user
        document.verified_at = timezone.now()
        document.notes = request.data.get('notes', document.notes)
        document.save()
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)


class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet for managing active loans."""
    
    queryset = Loan.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['loan_number', 'loan_application__customer__first_name', 'loan_application__customer__last_name']
    ordering_fields = ['disbursed_at', 'principal_amount', 'outstanding_balance']
    ordering = ['-disbursed_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LoanSummarySerializer
        return LoanSerializer
    
    @action(detail=True, methods=['post'])
    def make_payment(self, request, pk=None):
        """Record a payment for a loan."""
        loan = self.get_object()
        payment_amount = request.data.get('payment_amount')
        
        if not payment_amount:
            return Response(
                {'error': 'payment_amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        payment_amount = float(payment_amount)
        
        if payment_amount <= 0:
            return Response(
                {'error': 'payment_amount must be positive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if payment_amount > loan.outstanding_balance:
            payment_amount = loan.outstanding_balance
        
        loan.outstanding_balance -= payment_amount
        loan.total_paid += payment_amount
        
        if loan.outstanding_balance <= 0:
            loan.status = 'PAID_OFF'
            loan.outstanding_balance = 0
        
        loan.save()
        
        # Here you would typically create a Payment record
        # For now, we'll just return the updated loan
        
        serializer = self.get_serializer(loan)
        return Response(serializer.data)