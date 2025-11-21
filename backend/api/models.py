from mongoengine import (
    Document, StringField, FloatField, DateTimeField,
    BooleanField, ReferenceField, ListField, IntField, EmbeddedDocument,
    EmbeddedDocumentField
)
import datetime


# -----------------------------
# Category
# -----------------------------
class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField()


# -----------------------------
# FoodItem
# -----------------------------
class FoodItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image_url = StringField()
    category = ReferenceField(Category, required=True)
    customizations = ListField(StringField())  # simple MVP list of names
    created_at = DateTimeField(default=datetime.datetime.utcnow)


# -----------------------------
# OrderItem (embedded)
# -----------------------------
class OrderItem(EmbeddedDocument):
    food_id = StringField(required=True)  # store FoodItem.id as string
    name = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)  # snapshot price at purchase
    customizations = ListField(StringField())  # chosen customizations


# -----------------------------
# Order
# -----------------------------
class Order(Document):
    user_email = StringField(required=True)
    items = ListField(EmbeddedDocumentField(OrderItem))
    total = FloatField(required=True)
    status = StringField(default="pending")  # pending / confirmed / delivered
    created_at = DateTimeField(default=datetime.datetime.utcnow)
