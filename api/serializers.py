from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    image = serializers.CharField(required=False)

class FoodSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    price = serializers.FloatField()
    image = serializers.CharField(required=False)
    rating = serializers.FloatField(required=False)
    calories = serializers.IntegerField(required=False)
    protein = serializers.IntegerField(required=False)
    category = serializers.CharField()
    ingredients = serializers.ListField(required=False)
    cooking_time = serializers.CharField(required=False)
    is_veg = serializers.BooleanField(required=False)
    customizations = serializers.ListField(required=False)

class OrderItemSerializer(serializers.Serializer):
    food_id = serializers.CharField()
    name = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.FloatField()
    image = serializers.CharField(required=False)
    customizations = serializers.ListField(required=False)

class OrderSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_name = serializers.CharField(required=False)
    user_phone = serializers.CharField(required=False)
    items = OrderItemSerializer(many=True)
    total = serializers.FloatField()
    address = serializers.CharField(required=False)
    payment_method = serializers.CharField(required=False)