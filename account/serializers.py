from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.db.models import Q
from django.contrib.auth import authenticate
from account.backends import CustomAuthenticationBackend
from . models import User

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Get credentials
        email = attrs.get(self.username_field)
        password = attrs.get('password')
        
        if not email:
            raise serializers.ValidationError(
                {
                    'status': 'error',
                    'code': 'EMAIL_REQUIRED',
                    'message': 'Email or Username is required.'
                }
            )
            
        if not password:
            raise serializers.ValidationError(
                {
                    'status': 'error',
                    'code': 'PASSWORD_REQUIRED',
                    'message': 'Password is required.'
                }
            )
        
        # Check if user exists
        UserModel = User
        try:
            user_exists = UserModel.objects.filter(Q(email=email) | Q(user_name=email)).exists()
            if not user_exists:
                raise serializers.ValidationError(
                    {
                        'status': 'error',
                        'code': 'USER_NOT_FOUND',
                        'message': 'No account found with this email/username.'
                    }
                )
            
            # Attempt authentication
            user = self.user = authenticate(
                request=self.context.get('request'),
                username=email,  # Django uses username parameter regardless of actual field
                password=password
            )
            
            if not user:
                # User exists but password is incorrect
                raise serializers.ValidationError(
                    {
                        'status': 'error',
                        'code': 'INVALID_CREDENTIALS',
                        'message': 'Incorrect password.'
                    }
                )
            
            # Check if user is active
            if not user.is_active:
                raise serializers.ValidationError(
                    {
                        'status': 'error',
                        'code': 'ACCOUNT_INACTIVE',
                        'message': 'This account is inactive or unverified.'
                    }
                )
            
            # If we got here, authentication was successful
            data = super().validate(attrs)
            
            # Format the successful response
            return {
                'status': 'success',
                'message': 'Login successful',
                'access': data['access'],
                'refresh': data['refresh']
            }
            
        except UserModel.DoesNotExist:
            # This is a fallback and should not happen with the previous check
            raise serializers.ValidationError(
                {
                    'status': 'error',
                    'code': 'USER_NOT_FOUND',
                    'message': 'No account found with this email/username.'
                }
            )
            
            
class UserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, required=False, allow_null=True)
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "user_name", "image", "phone", "position", "is_user", "is_active", "password"]
        read_only_fields = ["phone", "position", "is_user", "is_active"]
        extra_kwargs = {
                    'password': {'write_only': True}
                }
        
    def create(self, validated_data):
        image = None
        if "image" in validated_data.keys():
            image = validated_data['image']
        user = User.objects.create(
                    email=validated_data['email'],
                    first_name=validated_data['first_name'],
                    last_name=validated_data['last_name'],
                    user_name = validated_data['user_name'],
                    is_user=True,
                    is_active=True,
                    image=image
                )
        
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # set email to read only on update
    def get_fields(self):
        fields = super().get_fields()
        if self.instance:
            fields['email'].read_only = True
        return fields
    
    
class UpdateUserSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=True, use_url=True, required=False, allow_null=True)
    class Meta:
        model= User
        fields = ["id", "email", "first_name", "last_name", "user_name", "phone", "position", "image", 'is_user', "is_active", 'is_admin']
        read_only_fields = ['email', 'is_user', 'is_active', 'is_admin']




class ChangePasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    