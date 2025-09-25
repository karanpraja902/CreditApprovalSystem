from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Customer, CustomerDocument
from .serializers import (
    CustomerSerializer, CustomerCreateSerializer,
    CustomerDocumentSerializer, CustomerSummarySerializer
)


class CustomerViewSet(viewsets.ModelViewSet):
    """ViewSet for managing customers."""
    
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'marital_status', 'employment_status', 'is_active']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = ['created_at', 'annual_income', 'last_name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CustomerCreateSerializer
        elif self.action == 'list':
            return CustomerSummarySerializer
        return CustomerSerializer
    
    @action(detail=True, methods=['get'])
    def documents(self, request, pk=None):
        """Get all documents for a specific customer."""
        customer = self.get_object()
        documents = CustomerDocument.objects.filter(customer=customer)
        serializer = CustomerDocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Advanced search for customers."""
        query = request.query_params.get('q', '')
        if not query:
            return Response({'error': 'Query parameter "q" is required'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        customers = Customer.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone_number__icontains=query)
        )
        
        serializer = CustomerSummarySerializer(customers, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def toggle_active(self, request, pk=None):
        """Toggle customer active status."""
        customer = self.get_object()
        customer.is_active = not customer.is_active
        customer.save()
        
        serializer = self.get_serializer(customer)
        return Response(serializer.data)


class CustomerDocumentViewSet(viewsets.ModelViewSet):
    """ViewSet for managing customer documents."""
    
    queryset = CustomerDocument.objects.all()
    serializer_class = CustomerDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['customer', 'document_type', 'is_verified']
    ordering_fields = ['uploaded_at']
    ordering = ['-uploaded_at']
    
    @action(detail=True, methods=['patch'])
    def verify(self, request, pk=None):
        """Verify a customer document."""
        document = self.get_object()
        document.is_verified = True
        document.verified_by = request.user
        from django.utils import timezone
        document.verified_at = timezone.now()
        document.save()
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'])
    def unverify(self, request, pk=None):
        """Unverify a customer document."""
        document = self.get_object()
        document.is_verified = False
        document.verified_by = None
        document.verified_at = None
        document.save()
        
        serializer = self.get_serializer(document)
        return Response(serializer.data)