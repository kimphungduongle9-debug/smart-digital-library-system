from rest_framework import serializers
from .models import User, Category, Document, DocumentAccess, Payment
from .models import DocumentAccess

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'avatar', 'role']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class DocumentSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'title', 'description', 'author',
            'published_year', 'category', 'category_detail',
            'cover_image', 'file',
            'price', 'popularity'
        ]

class DocumentAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentAccess
        fields = ['id', 'user', 'document', 'access_type', 'created_date']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'document', 'amount', 'method', 'status', 'created_date']
        read_only_fields = ['user', 'status', 'created_date']