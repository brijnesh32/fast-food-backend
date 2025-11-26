import datetime  # ADD THIS IMPORT AT THE TOP
from mongoengine import (
    Document, StringField, FloatField, DateTimeField,
    ReferenceField, ListField, IntField, EmbeddedDocument,
    EmbeddedDocumentField, BooleanField  # ADD BooleanField if needed
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