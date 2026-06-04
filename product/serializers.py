from rest_framework import serializers
from .models import Category,Product,Review
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from common.validators import validate_birthdate

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
        
class CatrgoryValidatorSerializer(serializers.Serializer):
    name = serializers.CharField(required=True,min_length=1,max_length=225) 

class ProductValidatorSerializer(serializers.Serializer):
    title = serializers.CharField(required=True,min_length=1,max_length=200)
    description = serializers.CharField(required=False, default="No text")
    price = serializers.IntegerField()
    category = serializers.IntegerField()

    def validate_category(self, category):
        try:
            Category.objects.get(id=category)
        except Category.DoesNotExist:
            raise ValidationError('Category does not exist!')
        return category
    
    def validate(self, attrs):
        token = self.context["request"].auth
        birthdate = token.get("birthdate")

        validate_birthdate(birthdate)

        return attrs

class ReviewValidatorSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, default="No text")
    product = serializers.IntegerField()
    stars = serializers.IntegerField()

    def validate_product(self, product):
        try:
            Product.objects.get(id=product)
        except Product.DoesNotExist:
            raise ValidationError('Product does not exist!')
        return product

