import os, json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from api.models import Category, FoodItem, Order, OrderItem
from api.serializers import RegisterSerializer, LoginSerializer, FoodSerializer, OrderSerializer
from api.utils import hash_password, verify_password, create_token, auth_required
@api_view(['GET'])
def health_check(request):
    return JsonResponse({'status':'ok','db':'connected'})
@api_view(['POST'])
def category_create(request):
    data = request.data
    if Category.objects(name=data.get('name')).first():
        return JsonResponse({'detail':'Category exists'}, status=400)
    c = Category(name=data.get('name'), description=data.get('description','')).save()
    return JsonResponse({'id':str(c.id)})
@api_view(['GET'])
def category_list(request):
    data = [{'id':str(c.id),'name':c.name,'description':c.description or ''} for c in Category.objects()]
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
    item = FoodItem(name=cd['name'], description=cd.get('description',''), price=cd['price'], image_url=cd.get('image_url',''), rating=cd.get('rating'), calories=cd.get('calories'), protein=cd.get('protein'), category=cat, customizations=cd.get('customizations',[])).save()
    return JsonResponse({'id':str(item.id)})
@api_view(['GET'])
def food_list(request):
    foods = FoodItem.objects()
    out = []
    for f in foods:
        out.append({'id':str(f.id),'name':f.name,'description':f.description,'price':f.price,'image_url':f.image_url,'rating':f.rating,'calories':f.calories,'protein':f.protein,'category':{'id':str(f.category.id),'name':f.category.name} if f.category else None,'customizations':f.customizations})
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
        order_items.append(OrderItem(food_id=it['food_id'], name=it['name'], quantity=it['quantity'], price=it['price'], customizations=it.get('customizations',[])))
    order = Order(user_email=cd['user_email'], items=order_items, total=cd['total']).save()
    return JsonResponse({'id':str(order.id)})
@api_view(['GET'])
def order_list(request):
    orders = Order.objects().order_by('-created_at')
    out = []
    for o in orders:
        out.append({'id':str(o.id),'user_email':o.user_email,'total':o.total,'status':o.status,'items':[{'food_id':it.food_id,'name':it.name,'quantity':it.quantity,'price':it.price,'customizations':it.customizations} for it in o.items]})
    return JsonResponse(out, safe=False)
@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload(request):
    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'detail':'File missing'}, status=400)
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, f.name)
    with open(path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    url = request.build_absolute_uri(settings.MEDIA_URL + 'uploads/' + f.name)
    return JsonResponse({'url':url})
