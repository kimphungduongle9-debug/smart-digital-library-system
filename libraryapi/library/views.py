from rest_framework import viewsets, generics, filters, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate

from .models import Category, Document
from .serializers import CategorySerializer, DocumentSerializer
from .paginators import DocumentPaginator
from .perms import IsVerifiedLibrarian

from rest_framework.decorators import action
from django.db.models import Count, Sum

from .models import Category, Document, DocumentAccess, Payment
from .serializers import CategorySerializer, DocumentSerializer, DocumentAccessSerializer, PaymentSerializer

class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer


class DocumentViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.RetrieveAPIView,
    generics.CreateAPIView,
    generics.UpdateAPIView,
    generics.DestroyAPIView
):
    queryset = Document.objects.filter(active=True)
    serializer_class = DocumentSerializer
    pagination_class = DocumentPaginator
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'author', 'description']
    ordering_fields = ['title', 'published_year', 'popularity']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsVerifiedLibrarian()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        query = self.queryset

        year = self.request.query_params.get('year')
        if year:
            query = query.filter(published_year=year)

        category_id = self.request.query_params.get('category_id')
        if category_id:
            query = query.filter(category_id=category_id)

        return query

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(methods=['get'], detail=False, url_path='stats')
    def stats(self, request):
        total_documents = Document.objects.filter(active=True).count()

        documents_by_category = Category.objects.annotate(
            total=Count('document')
        ).values('id', 'name', 'total')

        total_revenue = Payment.objects.filter(status='SUCCESS').aggregate(
            total=Sum('amount')
        )['total'] or 0

        return Response({
            'total_documents': total_documents,
            'documents_by_category': list(documents_by_category),
            'total_revenue': total_revenue
        })

    @action(methods=['post'], detail=True, url_path='access')
    def access(self, request, pk):
        document = self.get_object()

        access_type = request.data.get('access_type', 'VIEW')

        DocumentAccess.objects.create(
            user=request.user,
            document=document,
            access_type=access_type
        )

        document.popularity += 1
        document.save()

        return Response({
            'message': 'Access saved successfully',
            'document_id': document.id,
            'access_type': access_type
        })

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            return Response({
                'message': 'Login successful',
                'user_id': user.id,
                'username': user.username
            })

        return Response({'error': 'Invalid credentials'}, status=400)

class PaymentViewSet(
    viewsets.ViewSet,
    generics.ListAPIView,
    generics.CreateAPIView
):
    queryset = Payment.objects.all().order_by('-id')
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='SUCCESS')