from api.models import Category, FoodItem
from mongoengine import Document, StringField, FloatField, IntField, ListField, ReferenceField
from dummy_data import dummyData   # you will create this file

def seed_database():
    print("🚀 Starting seed...")

    # 1. Clear existing data
    Category.objects.delete()
    FoodItem.objects.delete()

    print("✔ Cleared old data")

    # 2. Insert Categories
    category_map = {}

    for cat in dummyData["categories"]:
        c = Category(
            name=cat["name"],
            description=cat["description"]
        ).save()

        category_map[cat["name"]] = c
    print("✔ Inserted categories")

    # 3. Insert Menu Items
    for item in dummyData["menu"]:
        category_obj = category_map.get(item["category_name"])

        food = FoodItem(
            name=item["name"],
            description=item["description"],
            image_url=item["image_url"],
            price=item["price"],
            rating=item["rating"],
            calories=item["calories"],
            protein=item["protein"],
            category=category_obj,
            customizations=item["customizations"],  # direct list of names
        )

        food.save()

    print("✔ Inserted menu items")
    print("🎉 Seeding Complete!")
