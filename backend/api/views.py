import os, json
from django.http import JsonResponse
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser

from api.models import Category, FoodItem, Order, OrderItem


# -----------------------------
# HEALTH CHECK
# -----------------------------
@api_view(["GET"])
def health_check(request):
    return JsonResponse({"status": "ok", "db": "connected"})


# -----------------------------
# CATEGORIES
# -----------------------------
@api_view(["POST"])
def category_create(request):
    data = request.data

    if Category.objects(name=data.get("name")).first():
        return JsonResponse({"detail": "Category exists"}, status=400)

    cat = Category(
        name=data.get("name"),
        description=data.get("description", "")
    ).save()

    return JsonResponse({"id": str(cat.id)})


@api_view(["GET"])
def category_list(request):
    data = [
        {
            "id": str(c.id),
            "name": c.name,
            "description": c.description or "",
        }
        for c in Category.objects()
    ]
    return JsonResponse(data, safe=False)


# -----------------------------
# FOOD ITEMS
# -----------------------------
@api_view(["POST"])
def food_create(request):
    data = request.data

    # validate category
    try:
        category = Category.objects.get(id=data.get("category"))
    except:
        return JsonResponse({"detail": "Invalid category"}, status=400)

    item = FoodItem(
        name=data.get("name"),
        description=data.get("description"),
        price=float(data.get("price")),
        image_url=data.get("image_url"),
        category=category,
        customizations=data.get("customizations", []),
    ).save()

    return JsonResponse({"id": str(item.id)})


@api_view(["GET"])
def food_list(request):
    foods = FoodItem.objects()

    data = [
        {
            "id": str(f.id),
            "name": f.name,
            "description": f.description,
            "price": f.price,
            "image_url": f.image_url,
            "category": {
                "id": str(f.category.id),
                "name": f.category.name
            } if f.category else None,
            "customizations": f.customizations
        }
        for f in foods
    ]
    return JsonResponse(data, safe=False)


# -----------------------------
# ORDERS
# -----------------------------
@api_view(["POST"])
def order_create(request):
    data = request.data

    items_payload = data.get("items", [])
    order_items = []

    for item in items_payload:
        order_items.append(
            OrderItem(
                food_id=item["food_id"],
                name=item["name"],
                quantity=item["quantity"],
                price=float(item["price"]),
                customizations=item.get("customizations", [])
            )
        )

    order = Order(
        user_email=data["user_email"],
        items=order_items,
        total=float(data["total"]),
        status="pending"
    ).save()

    return JsonResponse({"id": str(order.id)})


@api_view(["GET"])
def order_list(request):
    data = [
        {
            "id": str(o.id),
            "user_email": o.user_email,
            "total": o.total,
            "status": o.status,
            "items": [
                {
                    "food_id": it.food_id,
                    "name": it.name,
                    "quantity": it.quantity,
                    "price": it.price,
                    "customizations": it.customizations,
                }
                for it in o.items
            ]
        }
        for o in Order.objects().order_by("-created_at")
    ]

    return JsonResponse(data, safe=False)


# -----------------------------
# IMAGE UPLOAD
# -----------------------------
@api_view(["POST"])
@parser_classes([MultiPartParser])
def upload(request):
    f = request.FILES.get("file")
    if not f:
        return JsonResponse({"detail": "File missing"}, status=400)

    upload_dir = os.path.join(settings.MEDIA_ROOT, "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    path = os.path.join(upload_dir, f.name)

    with open(path, "wb+") as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    url = request.build_absolute_uri(settings.MEDIA_URL + "uploads/" + f.name)
    return JsonResponse({"url": url})
