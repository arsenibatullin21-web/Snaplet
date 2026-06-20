from django.contrib.auth import get_user_model, login, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError

from user.models import User
from rest_framework import serializers







class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email, password=password)
            if not user:
                raise serializers.ValidationError({
                    'error': "User is not found"
                })
            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError({
                'error': "Email or password is missing"
            })


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'phone', 'password', 'password_confirm']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        phone = attrs.get('phone')
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if get_user_model().objects.filter(username=username).exists():
            raise serializers.ValidationError({
                'error': "Username already exists"
            })
        if get_user_model().objects.filter(email=email).exists():
            raise serializers.ValidationError({
                'error': "Email already exists"
            })
        if get_user_model().objects.filter(phone=phone).exists():
            raise serializers.ValidationError({
                'error': "Phone number already exists"
            })
        if password != password_confirm:
            raise serializers.ValidationError({
                'error': "Passwords do not match"
            })
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'phone', 'followers_count', 'following_count']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'bio', 'avatar']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, validators=[validate_password, ])
    new_password_confirm = serializers.CharField(required=True)

    def validated_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({
                'error': "Old password is invalid"
            })
        return value

    def validate(self, attrs):
        password1 = attrs.get('new_password')
        password2 = attrs.get('new_password_confirm')
        if password1 != password2:
            raise serializers.ValidationError({
                'error': "Password do not match"
            })
        return attrs





