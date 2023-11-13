from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Category,Order
from .serializers import CategorySerializer,OrderSerializer
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView,RetrieveUpdateAPIView,CreateAPIView,RetrieveAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }




class Category_views(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class Data(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
class Order_views(APIView):
    def get(self, request, id=None, format=None):
        if id:
            obj=Order.objects.get(id=id)
            serializer=OrderSerializer(obj)
            return Response(serializer.data)
        obj=Order.objects.all()
        serializer=OrderSerializer(obj,many=True)
        return Response(serializer.data)
    def post(self, request, id=None, format=None):
        data = request.data
        catName=Category.objects.get(id=data['cate_name'])
        type = Order.objects.create(name= data['name'],cate_name=catName)
        type.save()
        serializer = OrderSerializer(type, many=False)
        return Response(serializer.data)
    def post(self, request, id=None, format=None):
        data = request.data
        catName=Category.objects.get(id=data['cate_name'])
        type = Order.objects.create(name= data['name'],cate_name=catName)
        type.save()
        serializer = OrderSerializer(type, many=False)
        return Response(serializer.data)
    def delete(self,request, id=None):
        print(id)
        type = Order.objects.get(id = id)
        type.delete()
        return Response("Type Deleted!")
@api_view(['POST'])
@csrf_exempt
def userlogin(request):
    name=request.POST['name']
    password=request.POST['password']
    user = authenticate(username=name, password=password)
    if user is not None:
        token=get_tokens_for_user(user)
        login(request, user)
        return Response({"id":user.id,"token":token})
    else:
        return Response("Login Failed")