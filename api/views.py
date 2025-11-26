import os, json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from api.models import Category, FoodItem, Order, OrderItem
from api.serializers import FoodSerializer, OrderSerializer
from api.utils import auth_required

@api_view(['GET'])
def health_check(request):
    return JsonResponse({'status':'ok','db':'connected'})

@api_view(['POST'])
def category_create(request):
    data = request.data
    if Category.objects(name=data.get('name')).first():
        return JsonResponse({'detail':'Category exists'}, status=400)
    c = Category(
        name=data.get('name'), 
        description=data.get('description',''),
        image=data.get('image','')  # ADD THIS
    ).save()
    return JsonResponse({'id':str(c.id)})

@api_view(['GET'])
def category_list(request):
    data = [{
        'id':str(c.id),
        'name':c.name,
        'description':c.description or '',
        'image': c.image or ''  # ADD THIS
    } for c in Category.objects()]
    return JsonResponse(data, safe=False)

@api_view(['POST'])
@auth_required
def food_create(request):
    s = FoodSerializer(data=request.data)
    if not s.is_valid():
        return JsonResponse(s.errors, status=400)
    cd = s.validated_data
    try:
        cat = Category.objects.get(id=cd['category'])
    except Exception:
        return JsonResponse({'detail':'Invalid category'}, status=400)
    
    item = FoodItem(
        name=cd['name'], 
        description=cd.get('description',''), 
        price=cd['price'], 
        image=cd.get('image',''),  # CHANGED from image_url
        rating=cd.get('rating', 0),
        calories=cd.get('calories', 0),
        protein=cd.get('protein', 0),
        category=cat,
        ingredients=cd.get('ingredients', []),  # ADD THIS
        cooking_time=cd.get('cooking_time', ''),  # ADD THIS
        is_veg=cd.get('is_veg', False),  # ADD THIS
        customizations=cd.get('customizations',[])
    ).save()
    return JsonResponse({'id':str(item.id)})

@api_view(['GET'])
def food_list(request):
    foods = FoodItem.objects()
    out = []
    for f in foods:
        out.append({
            'id':str(f.id),
            'name':f.name,
            'description':f.description,
            'price':f.price,
            'image': f.image or '',  # CHANGED from image_url
            'rating':f.rating,
            'calories':f.calories,
            'protein':f.protein,
            'category':{
                'id':str(f.category.id),
                'name':f.category.name
            } if f.category else None,
            'ingredients': f.ingredients or [],  # ADD THIS
            'cooking_time': f.cooking_time or '',  # ADD THIS
            'is_veg': f.is_veg or False,  # ADD THIS
            'customizations':f.customizations
        })
    return JsonResponse(out, safe=False)

@api_view(['POST'])
def order_create(request):
    s = OrderSerializer(data=request.data)
    if not s.is_valid():
        return JsonResponse(s.errors, status=400)
    cd = s.validated_data
    items_payload = cd['items']
    order_items = []
    for it in items_payload:
        order_items.append(OrderItem(
            food_id=it['food_id'], 
            name=it['name'], 
            quantity=it['quantity'], 
            price=it['price'], 
            image=it.get('image', ''),  # ADD THIS
            customizations=it.get('customizations',[])
        ))
    order = Order(
        user_email=cd['user_email'],
        user_name=cd.get('user_name', ''),  # ADD THIS
        user_phone=cd.get('user_phone', ''),  # ADD THIS
        items=order_items, 
        total=cd['total'],
        address=cd.get('address', ''),  # ADD THIS
        payment_method=cd.get('payment_method', 'card')  # ADD THIS
    ).save()
    return JsonResponse({'id':str(order.id)})

@api_view(['GET'])
def order_list(request):
    orders = Order.objects().order_by('-created_at')
    out = []
    for o in orders:
        out.append({
            'id':str(o.id),
            'user_email':o.user_email,
            'user_name': o.user_name or '',  # ADD THIS
            'user_phone': o.user_phone or '',  # ADD THIS
            'total':o.total,
            'status':o.status,
            'address': o.address or '',  # ADD THIS
            'payment_method': o.payment_method or 'card',  # ADD THIS
            'items':[{
                'food_id':it.food_id,
                'name':it.name,
                'quantity':it.quantity,
                'price':it.price,
                'image': it.image or '',  # ADD THIS
                'customizations':it.customizations
            } for it in o.items]
        })
    return JsonResponse(out, safe=False)

# ADD THESE NEW ENDPOINTS
@api_view(['GET'])
def featured_foods(request):
    """Get featured foods for home screen"""
    foods = FoodItem.objects().order_by('-rating')[:8]
    out = []
    for f in foods:
        out.append({
            'id': str(f.id),
            'name': f.name,
            'price': f.price,
            'image': f.image or '',
            'rating': f.rating or 0,
            'cooking_time': f.cooking_time or ''
        })
    return JsonResponse(out, safe=False)

@api_view(['GET'])
def search_foods(request):
    """Search foods by name"""
    query = request.GET.get('q', '')
    if query:
        foods = FoodItem.objects(name__icontains=query)
    else:
        foods = FoodItem.objects()
    
    out = []
    for f in foods:
        out.append({
            'id': str(f.id),
            'name': f.name,
            'price': f.price,
            'image': f.image or '',
            'rating': f.rating or 0
        })
    return JsonResponse(out, safe=False)