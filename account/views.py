from django.conf import settings
from django.shortcuts import render
import requests
from django.contrib.auth import authenticate
from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework import status
from drf_yasg import openapi
from django.urls import reverse
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
import random
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from datetime import timedelta
from django.core.mail import send_mail
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.views import TokenObtainPairView
from account.models import User
from . serializers import MyTokenObtainPairSerializer, UserSerializer, ResetPasswordSerializer, UpdateUserSerializer, ChangePasswordSerializer, ForgotPasswordSerializer
from rest_framework.permissions import IsAuthenticated
import uuid
from rest_framework_simplejwt.views import TokenObtainPairView


@swagger_auto_schema(method='POST', request_body=UserSerializer)
@api_view(['POST'])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def register_user(request):
    data = request.data
    user_serializer = UserSerializer(data=data)
    
    try:
        if user_serializer.is_valid(raise_exception=False):
            # Check if email already exists
            UserModel = User
            email = data.get('email')
            user_name = data.get('user_name')
            if email and UserModel.objects.filter(email=email).exists():
                return Response({
                    'status': 'error',
                    'code': 'EMAIL_EXISTS',
                    'message': 'A user with this email already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)
            if user_name and UserModel.objects.filter(user_name=email).exists():
                return Response({
                    'status': 'error',
                    'code': 'USERNAME_EXISTS',
                    'message': 'A user with this username already exists.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user = user_serializer.save()
            user.save()
        
            return Response({
                'status': 'success',
                'message': 'User Account Created Successfully.',
                'user': user_serializer.data
            }, status=status.HTTP_201_CREATED)
        else:
            # Process validation errors
            errors = user_serializer.errors
            error_type = next(iter(errors))
            error_message = errors[error_type][0]
            
            error_codes = {
                'email': 'INVALID_EMAIL',
                'password': 'INVALID_PASSWORD',
                'user_name': 'INVALID_USERNAME',
                'non_field_errors': 'VALIDATION_ERROR'
            }
            
            return Response({
                'status': 'error',
                'code': error_codes.get(error_type, 'VALIDATION_ERROR'),
                'field': error_type,
                'message': error_message
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        return Response({
            'status': 'error',
            'code': 'SERVER_ERROR',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@swagger_auto_schema(method='PUT', request_body=UpdateUserSerializer)
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
@parser_classes([JSONParser, MultiPartParser, FormParser])
def user_details(request):
    if request.method == "GET":
        
        user_serializer = UserSerializer(request.user)
        data = user_serializer.data
        return Response(data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        user_serializer = UpdateUserSerializer(request.user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_202_ACCEPTED)
        

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='The user\'s password for verification')
        },
        required=['password']
    ),
    responses={
        200: openapi.Response('User account deactivated successfully.'),
        400: openapi.Response('Invalid password or bad request.')
    },
    operation_description="Deactivate user account by verifying the password."
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deactivate_user(request):
    user = request.user
    password = request.data.get('password')

    if not password:
        return JsonResponse({'message': 'Password is required.'}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate the user
    user_check = authenticate(username=user.email, password=password)
    
    if user_check is None:
        return JsonResponse({'message': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)

    # Deactivate the user
    user.is_active = False
    user.save()

    return JsonResponse({'message': 'User account deactivated successfully.'})
    
    
@swagger_auto_schema(method='POST', request_body=ChangePasswordSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = request.user
    old_password = serializer.validated_data['old_password']
    new_password = serializer.validated_data['new_password']
    
    if not user.check_password(old_password):
        return Response({'message': 'Old password is incorrect.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user.set_password(new_password)
    user.save()
    
    return Response({'message': 'Password updated successfully.'}, status=status.HTTP_200_OK)