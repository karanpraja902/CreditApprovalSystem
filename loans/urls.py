from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanProductViewSet, LoanApplicationViewSet, LoanDocumentViewSet, LoanViewSet

router = DefaultRouter()
router.register(r'products', LoanProductViewSet)
router.register(r'applications', LoanApplicationViewSet)
router.register(r'documents', LoanDocumentViewSet)
router.register(r'loans', LoanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]