from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Category,Product,Review
from .serializers import CategoryListSerializer,ProductListSerializer,ReviewsListSerializer
from django.db.models import Count

@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.annotate(products_count=Count('product') )
    data = CategoryListSerializer(categories,many=True).data

    return Response(
        data=data,  
        status=status.HTTP_200_OK,  
    )

@api_view(['GET'])
def category_api_view(request,id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = CategoryListSerializer(category,many=False).data
    return Response(data=data)


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data = ProductListSerializer(products,many=True).data
    return Response(
        data=data,
        status=status.HTTP_200_OK,
    )
  
@api_view(['GET'])
def product_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    data = ProductListSerializer(product,many=False).data
    return Response(data=data)

@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data = ReviewsListSerializer(reviews,many=True).data
    return Response(data=data)

@api_view(['GET'])
def review_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status.HTTP_404_NOT_FOUND)
    data = ReviewsListSerializer(review,many=False).data
    return Response(data=data)
