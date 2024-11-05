from django.contrib.auth.password_validation import validate_password

from userauths.models import AgentProfile, User, TenantProfile
from api import models as api_model

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['full_name'] = user.full_name
        token['email'] = user.email
        token['username'] = user.username        

        return token

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'password2', 'user_type']

    def validate(self, attr):
        if attr['password'] != attr['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attr
    
    def create(self, validated_data):
        user = User.objects.create(
            full_name=validated_data['full_name'],
            email=validated_data['email']
        )
        email_username, _ = user.email.split("@")
        user.username = email_username
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """Doc"""
    class Meta:
        model = User
        fields = '__all__'


class AgentProfileSerializer(serializers.ModelSerializer):
    """Doc"""
    class Meta:
        model = AgentProfile
        fields = '__all__'

class TenantProfileSerializer(serializers.ModelSerializer):
    """Doc"""
    class Meta:
        model = AgentProfile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_model.Category

class ReviewSerializer(serializers.ModelSerializer):
    profile = TenantProfileSerializer(many=True)

    class Meta:
        fields = ['user', 'property', 'rating', 'review_text', 'reply', 'profile']
        model = api_model.Review

class PropertySerializer(serializers.ModelSerializer):
    tenant = UserSerializer(many=True)
    review = ReviewSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = api_model.Property


class PropertyImageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_model.PropertyImage


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_model.Booking


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = api_model.Message


class SavedSearchSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_model.SavedSearch


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_model.Transaction


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = api_model.Notification

class InquirySerializer(serializers.ModelSerializer):
    profile = TenantProfileSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = api_model.Inquiry

