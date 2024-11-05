import random
from django.shortcuts import render

from userauths.models import User, AgentProfile, TenantProfile
from api import serializer as api_serializer
from api import models as api_models

from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import action


class ApiRootView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the NestFinder API!"})


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializer.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializer.RegisterSerializer


def generate_random_otp(Length=7):
    otp = ''.join([str(random.randint(0, 9)) for _ in range(Length)])
    return otp


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classess = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def get_object(self):
        email = self.kwargs['email']
        user = User.objects.filter(email=email).first()

        if user:
            uuidb64 = user.pk
            refresh = RefreshToken.for_user(user)
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            link = f'localhost:5173/create-new-password/?otp={user.otp}&uuidb64={uuidb64}&=refresh_token{refresh_token}'
            print("link =====", link)
        return user
    

class PasswordchangeAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializer.UserSerializer

    def create(self, request, *args, **kwargs):
        otp = request.data['otp']
        uuidb64 = request.data['uuidb64']
        password = request.data['password']

        user = User.objects.get(id=uuidb64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ""
            user.save()    

            return Response({"message": "Password Changed Successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User Does Not Exists"}, status=status.HTTP_404_NOT_FOUND)
        
"""class AgentListAPIView(generics.ListAPIView):
    queryset = api_models.Agent.objects.all()
    serializer_class = api_serializer.AgentSerializer
    permission_class = [AllowAny]

    @action(detail=False, methods=['GET'])
    def me(self, request):
        agent = self.queryset.get(user=request.user)
        serializer = self.get_serializer(agent)
        return Response(serializer.data)
"""

class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.all()
    serializer_class = api_serializer.CategorySerializer
    permission_classes = [AllowAny]


class PropertyListAPIView(generics.ListAPIView):
    queryset = api_models.Property.objects.all()
    serializer_class = api_serializer.PropertySerializer
    permission_classes = [AllowAny]

