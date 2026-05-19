from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Category,Product,Review
from .serializers import CategoryListSerializer,ProductListSerializer,ReviewsListSerializer,CatrgoryValidatorSerializer,ProductValidatorSerializer,ReviewValidatorSerializer
from django.db.models import Count
from django.db import transaction
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet



class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer


class CategoryAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    lookup_field = 'id'


class ProductListAPIView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class ProductAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    lookup_field = 'id'


class ReviewListAPIView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsListSerializer
    

class ReviewAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewsListSerializer
    lookup_field = 'id'



# @api_view(['GET', 'POST'])
# def category_list_api_view(request):
#     print(request.user)
#     if request.method == 'GET':
#         categories = Category.objects.annotate(products_count=Count('product') )
#         data = CategoryListSerializer(categories,many=True).data

#         return Response(
#             data=data,  
#             status=status.HTTP_200_OK,  
#         )
#     elif request.method == 'POST':
#         serializer = CatrgoryValidatorSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)

#         name = serializer.validated_data.get('name')

#         category = Category.objects.create(name=name)
#         category.save()

#         return Response(status=status.HTTP_201_CREATED, data=CategoryListSerializer(category).data)

# @api_view(['GET','PUT', 'DELETE'])
# def category_api_view(request,id):
#     try:
#         category = Category.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = CategoryListSerializer(category,many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         category.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         serializer = CatrgoryValidatorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         category.name = serializer.validated_data.get('name')
#         category.save()
#         return Response(status=status.HTTP_201_CREATED,data=CategoryListSerializer(category).data)



# @api_view(['GET','POST'])
# def product_list_api_view(request):
#     if request.method == 'GET':
#         products = Product.objects.all()
#         data = ProductListSerializer(products,many=True).data
#         return Response(
#             data=data,
#             status=status.HTTP_200_OK,
#         )
#     elif request.method == 'POST':
#         serializer = ProductValidatorSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)

#         title = serializer.validated_data.get('title')
#         description = serializer.validated_data.get('description')
#         price = serializer.validated_data.get('price')
#         category = serializer.validated_data.get('category')

#         product = Product.objects.create(title=title,description=description,price=price,category_id=category,)
#         product.save()

#         return Response(status=status.HTTP_201_CREATED,data=ProductListSerializer(product).data)
  
# @api_view(['GET','PUT','DELETE'])
# def product_api_view(request,id):
#     try:
#         product = Product.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ProductListSerializer(product,many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     else:
#         serializer = ProductValidatorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         product.title = serializer.validated_data.get('title')
#         product.description = serializer.validated_data.get('description')
#         product.price = serializer.validated_data.get('price')
#         product.category_id = serializer.validated_data.get('category')
#         product.save()

#         return Response(status=status.HTTP_201_CREATED,data=ProductListSerializer(product).data)



# @api_view(['GET','POST'])
# def review_list_api_view(request):
#     if request.method == 'GET':
#         reviews = Review.objects.all()
#         data = ReviewsListSerializer(reviews,many=True).data
#         return Response(data=data)
#     elif request.method == 'POST':
#         serializer = ReviewValidatorSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(status=status.HTTP_400_BAD_REQUEST,
#                             data=serializer.errors)

#         text = serializer.validated_data.get('text')
#         product = serializer.validated_data.get('product')
#         stars = serializer.validated_data.get('stars')

#         reviews = Review.objects.create(text=text,product_id=product,stars=stars)
#         reviews.save()

#         return Response (status=status.HTTP_201_CREATED,data=ReviewsListSerializer(reviews).data)

# @api_view(['GET','PUT','DELETE'])
# def review_api_view(request,id):
#     try:
#         review = Review.objects.get(id=id)
#     except:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data = ReviewsListSerializer(review,many=False).data
#         return Response(data=data)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     elif request.method == 'PUT':
#         serializer = ReviewValidatorSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         review.text = serializer.validated_data.get('text')
#         review.product_id = rserializer.validated_data.get('product')
#         review.stars = serializer.validated_data.get('stars')
#         review.save()

#         return Response(status=status.HTTP_201_CREATED,data=ReviewsListSerializer(review).data)
