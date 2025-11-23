import datetime
from mongoengine import (
    Document, StringField, FloatField, DateTimeField,
    ReferenceField, ListField, IntField, EmbeddedDocument,
    EmbeddedDocumentField
)
class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
class FoodItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image_url = StringField()
    rating = FloatField()
    calories = IntField()
    protein = IntField()
    category = ReferenceField(Category, required=True)
    customizations = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.utcnow)
class OrderItem(EmbeddedDocument):
    food_id = StringField(required=True)
    name = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    customizations = ListField(StringField())
class Order(Document):
    user_email = StringField(required=True)
    items = ListField(EmbeddedDocumentField(OrderItem))
    total = FloatField(required=True)
    status = StringField(default='pending')
    created_at = DateTimeField(default=datetime.datetime.utcnow)
