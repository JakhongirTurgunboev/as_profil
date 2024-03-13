# users/serializers.py
from rest_framework import serializers, validators
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=200, write_only=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = super(CustomUserSerializer, self).create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class CustomLoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    password = serializers.CharField(max_length=15)


class CustomRefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(max_length=250)