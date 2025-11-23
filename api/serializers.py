from rest_framework import serializers
class RegisterSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
class FoodSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.FloatField()
    image_url = serializers.CharField(required=False, allow_blank=True)
    rating = serializers.FloatField(required=False)
    calories = serializers.IntegerField(required=False)
    protein = serializers.IntegerField(required=False)
    category = serializers.CharField()
    customizations = serializers.ListField(child=serializers.CharField(), required=False)
class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    customizations = serializers.ListField(child=serializers.CharField(), required=False)
class OrderSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    items = OrderItemSerializer(many=True)
    total = serializers.FloatField()
