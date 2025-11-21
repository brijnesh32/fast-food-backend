from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class FoodSerializer(serializers.Serializer):
    id = serializers.CharField(required=False)
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.FloatField()
    image_url = serializers.CharField(required=False, allow_blank=True)
    category = serializers.CharField(required=False, allow_blank=True)

class OrderSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    items = serializers.CharField()
    total = serializers.FloatField()
