import time
import requests

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from auth_api.models import User
from auth_api.serializers import UserRegistrationSerializer, UserLoginSerializer


class SignUpView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                email=serializer.validated_data.get('email'),
                phone=serializer.validated_data.get('phone'),
                password=serializer.validated_data['password'],
                id_type=serializer.validated_data['id_type']
            )
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignInView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            id_value = serializer.validated_data['id']
            user = User.objects.filter(email=id_value).first() or User.objects.filter(phone=id_value).first()
            
            if user and user.check_password(serializer.validated_data['password']):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class UserInfoView(APIView):
    def get(self, request):
        user = request.user
        return Response({
            'id': user.email or user.phone,
            'id_type': user.id_type
        })


class LatencyView(APIView):
    def get(self, request):
        start_time = time.time()
        requests.get('https://ya.ru')
        latency = int((time.time() - start_time) * 1000)
        return Response({'latency': f'{latency}ms'})


class LogoutView(APIView):
    def post(self, request):
        if request.data.get('all'):
            request.user.auth_token_set.all().delete()
        else:
            request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
