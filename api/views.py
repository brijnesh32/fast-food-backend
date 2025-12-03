import os, json
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser
from api.models import Category, FoodItem, Order, OrderItem
from api.serializers import FoodSerializer, OrderSerializer
from api.utils import auth_required 
import hashlib
import secrets
from .models import User, UserSession
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

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
        image=data.get('image','')
    ).save()
    return JsonResponse({'id':str(c.id)})

@api_view(['GET'])
def category_list(request):
    data = [{
        'id':str(c.id),
        'name':c.name,
        'description':c.description or '',
        'image': c.image or ''
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
        image=cd.get('image',''),
        rating=cd.get('rating', 0),
        calories=cd.get('calories', 0),
        protein=cd.get('protein', 0),
        category=cat,
        ingredients=cd.get('ingredients', []),
        cooking_time=cd.get('cooking_time', ''),
        is_veg=cd.get('is_veg', False),
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
            'image': f.image or '',
            'rating':f.rating,
            'calories':f.calories,
            'protein':f.protein,
            'category':{
                'id':str(f.category.id),
                'name':f.category.name
            } if f.category else None,
            'ingredients': f.ingredients or [],
            'cooking_time': f.cooking_time or '',
            'is_veg': f.is_veg or False,
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
            image=it.get('image', ''),
            customizations=it.get('customizations',[])
        ))
    order = Order(
        user_email=cd['user_email'],
        user_name=cd.get('user_name', ''),
        user_phone=cd.get('user_phone', ''),
        items=order_items, 
        total=cd['total'],
        address=cd.get('address', ''),
        payment_method=cd.get('payment_method', 'card')
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
            'user_name': o.user_name or '',
            'user_phone': o.user_phone or '',
            'total':o.total,
            'status':o.status,
            'address': o.address or '',
            'payment_method': o.payment_method or 'card',
            'items':[{
                'food_id':it.food_id,
                'name':it.name,
                'quantity':it.quantity,
                'price':it.price,
                'image': it.image or '',
                'customizations':it.customizations
            } for it in o.items]
        })
    return JsonResponse(out, safe=False)

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

@api_view(['POST'])
@parser_classes([MultiPartParser])
def upload(request):
    f = request.FILES.get('file')
    if not f:
        return JsonResponse({'detail':'File missing'}, status=400)
    
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Create a unique filename to avoid conflicts
    import uuid
    file_extension = os.path.splitext(f.name)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    path = os.path.join(upload_dir, unique_filename)
    
    with open(path, 'wb+') as dest:
        for chunk in f.chunks():
            dest.write(chunk)
    
    url = request.build_absolute_uri(settings.MEDIA_URL + 'uploads/' + unique_filename)
    return JsonResponse({'url': url})

@api_view(['POST'])
def seed_database(request):
    """Seed database with dummy data"""
    try:
        from api.dummy_data import dummyData
        from api.models import Category, FoodItem
        
        # Clear existing data
        Category.objects.delete()
        FoodItem.objects.delete()
        
        # Create Categories
        categories_map = {}
        for cat_data in dummyData['categories']:
            category = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                image=""
            )
            category.save()
            categories_map[cat_data['name']] = category
        
        # Create Food Items
        for food_data in dummyData['menu']:
            food_item = FoodItem(
                name=food_data['name'],
                description=food_data['description'],
                image=food_data['image_url'],
                price=food_data['price'],
                rating=food_data['rating'],
                calories=food_data['calories'],
                protein=food_data['protein'],
                category=categories_map[food_data['category_name']],
                ingredients=[],
                cooking_time="15-20 mins",
                is_veg=False,
                customizations=food_data['customizations']
            )
            food_item.save()
        
        return JsonResponse({'status': 'success', 'message': 'Database seeded with sample data'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt    
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '').strip()
        
        # Find user
        user = User.objects(email=email).first()
        if not user:
            return JsonResponse({
                'ok': False,
                'message': 'Invalid email or password'
            }, status=401)
        
        # Check password (simple hash for now)
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return JsonResponse({
                'ok': False,
                'message': 'Invalid email or password'
            }, status=401)
        
        # Create session
        token = secrets.token_hex(32)
        session = UserSession(
            user_id=str(user.id),
            token=token,
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )
        session.save()
        
        return JsonResponse({
            'ok': True,
            'token': token,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_POST
def register_view(request):
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        password = data.get('password', '').strip()
        
        # Check if user exists
        if User.objects(email=email).first():
            return JsonResponse({
                'ok': False,
                'message': 'User already exists'
            }, status=400)
        
        # Create user
        user = User(
            email=email,
            name=name
        )
        user.password_hash = hashlib.sha256(password.encode()).hexdigest()
        user.save()
        
        # Auto login after registration
        token = secrets.token_hex(32)
        session = UserSession(
            user_id=str(user.id),
            token=token,
            expires_at=datetime.datetime.utcnow() + datetime.timedelta(days=7)
        )
        session.save()
        
        return JsonResponse({
            'ok': True,
            'token': token,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'ok': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_POST
def logout_view(request):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if token:
            session = UserSession.objects(token=token).first()
            if session:
                session.is_active = False
                session.save()
        
        return JsonResponse({'ok': True, 'message': 'Logged out successfully'})
        
    except Exception as e:
        return JsonResponse({'ok': False, 'message': str(e)}, status=500)

@csrf_exempt
def get_profile(request):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return JsonResponse({'ok': False, 'message': 'No token provided'}, status=401)
        
        # Find active session
        session = UserSession.objects(token=token, is_active=True).first()
        if not session:
            return JsonResponse({'ok': False, 'message': 'Invalid token'}, status=401)
        
        # Check if expired
        if session.expires_at < datetime.datetime.utcnow():
            session.is_active = False
            session.save()
            return JsonResponse({'ok': False, 'message': 'Session expired'}, status=401)
        
        # Get user
        user = User.objects(id=session.user_id).first()
        if not user:
            return JsonResponse({'ok': False, 'message': 'User not found'}, status=404)
        
        return JsonResponse({
            'ok': True,
            'user': {
                'id': str(user.id),
                'email': user.email,
                'name': user.name
            }
        })
        
    except Exception as e:
        return JsonResponse({'ok': False, 'message': str(e)}, status=500)