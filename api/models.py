import datetime
from mongoengine import (
    Document, StringField, FloatField, DateTimeField,
    ReferenceField, ListField, IntField, EmbeddedDocument,
    EmbeddedDocumentField, BooleanField
)

class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    image = StringField()

class FoodItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image = StringField()
    rating = FloatField(default=0)
    calories = IntField(default=0)
    protein = IntField(default=0)
    category = ReferenceField(Category, required=True)
    ingredients = ListField(StringField())
    cooking_time = StringField()
    is_veg = BooleanField(default=False)
    customizations = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class OrderItem(EmbeddedDocument):
    food_id = StringField(required=True)
    name = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    image = StringField()
    customizations = ListField(StringField())

class Order(Document):
    user_email = StringField(required=True)
    user_name = StringField()
    user_phone = StringField()
    items = ListField(EmbeddedDocumentField(OrderItem))
    total = FloatField(required=True)
    status = StringField(default='pending')
    address = StringField()
    payment_method = StringField(default='card')
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    delivery_option = StringField(default='delivery')  # 'delivery' or 'dine-in'
    restaurant_name = StringField(default='')
    restaurant_address = StringField(default='')
    pincode = StringField(default='')



class User(Document):
    email = StringField(required=True, unique=True)
    password_hash = StringField(required=True)
    name = StringField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    is_active = BooleanField(default=True)

    meta = {
        'collection': 'users',
        'indexes': ['email']
    }

class UserSession(Document):
    user_id = StringField(required=True)
    token = StringField(required=True, unique=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow)
    expires_at = DateTimeField(required=True)
    is_active = BooleanField(default=True)

    meta = {
        'collection': 'user_sessions',
        'indexes': ['token', 'user_id']
    }