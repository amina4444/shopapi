from rest_framework import serializers
from .models import Category,Product,Review

class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        
class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "id text".split()
