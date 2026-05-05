from rest_framework import serializers
from .models import Category,Product,Review
from django.db.models import Avg

class CategoryListSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Category
        fields = 'id  name products_count'.split()


class ReviewsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "id text".split()

class ProductListSerializer(serializers.ModelSerializer):
    reviews = ReviewsListSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = 'id title description price category rating reviews'.split()

    def get_rating(self, obj):
        return obj.reviews.aggregate(avg=Avg('stars'))['avg']
        

