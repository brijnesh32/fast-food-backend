from mongoengine import *

class Category(Document):
    name = StringField(required=True, unique=True)
    description = StringField()
    image = StringField()  # Add this for category images

class FoodItem(Document):
    name = StringField(required=True)
    description = StringField()
    price = FloatField(required=True)
    image = StringField()  # Change from image_url to image
    rating = FloatField(default=0)
    calories = IntField(default=0)
    protein = IntField(default=0)
    category = ReferenceField(Category, required=True)
    ingredients = ListField(StringField())  # Add ingredients
    cooking_time = StringField()  # Add cooking time
    is_veg = BooleanField(default=False)  # Add veg/non-veg
    customizations = ListField(StringField())
    created_at = DateTimeField(default=datetime.datetime.utcnow)

class OrderItem(EmbeddedDocument):
    food_id = StringField(required=True)
    name = StringField(required=True)
    quantity = IntField(required=True)
    price = FloatField(required=True)
    image = StringField()  # Add image for order items
    customizations = ListField(StringField())

class Order(Document):
    user_email = StringField(required=True)
    user_name = StringField()  # Add user name
    user_phone = StringField()  # Add phone number
    items = ListField(EmbeddedDocumentField(OrderItem))
    total = FloatField(required=True)
    status = StringField(default='pending')
    address = StringField()  # Add delivery address
    payment_method = StringField(default='card')
    created_at = DateTimeField(default=datetime.datetime.utcnow)