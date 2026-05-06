from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Category,Product,Review
from .serializers import CategoryListSerializer,ProductListSerializer,ReviewsListSerializer
from django.db.models import Count

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.annotate(products_count=Count('product') )
        data = CategoryListSerializer(categories,many=True).data

        return Response(
            data=data,  
            status=status.HTTP_200_OK,  
        )
    elif request.method == 'POST':
        name = request.data.get('name')

        category = Category.objects.create(name=name)
        category.save()

        return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializer(category).data)

@api_view(['GET','PUT', 'DELETE'])
def category_api_view(request,id):
    try:
        category = Category.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = CategoryListSerializer(category,many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_201_CREATED,data=CategoryListSerializer(category).data)



@api_view(['GET','POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data = ProductListSerializer(products,many=True).data
        return Response(
            data=data,
            status=status.HTTP_200_OK,
        )
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category = request.data.get('category')

        product = Product.objects.create(title=title,description=description,price=price,category_id=category,)
        product.save()

        return Response(status=status.HTTP_201_CREATED,data=ProductListSerializer(product).data)
  
@api_view(['GET','PUT','DELETE'])
def product_api_view(request,id):
    try:
        product = Product.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ProductListSerializer(product,many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category')
        product.save()

        return Response(status=status.HTTP_201_CREATED,data=ProductListSerializer(product).data)



@api_view(['GET','POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data = ReviewsListSerializer(reviews,many=True).data
        return Response(data=data)
    elif request.method == 'POST':
        text = request.data.get('text')
        product = request.data.get('product')
        stars = request.data.get('stars')

        reviews = Review.objects.create(text=text,product_id=product,stars=stars)
        reviews.save()

        return Response (status=status.HTTP_201_CREATED,data=ReviewsListSerializer(reviews).data)

@api_view(['GET','PUT','DELETE'])
def review_api_view(request,id):
    try:
        review = Review.objects.get(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data = ReviewsListSerializer(review,many=False).data
        return Response(data=data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.product_id = request.data.get('product')
        review.stars = request.data.get('stars')
        review.save()

        return Response(status=status.HTTP_201_CREATED,data=ReviewsListSerializer(review).data)
