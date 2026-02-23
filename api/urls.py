from django.urls import path
from . import views

urlpatterns = [
    path('health/', views.health_check),
    path('categories/', views.category_list),
    path('categories/create/', views.category_create),
    path('foods/', views.food_list),
    path('foods/create/', views.food_create),
    path('foods/featured/', views.featured_foods),
    path('foods/search/', views.search_foods),
    
    # ✅ ORDER ENDPOINTS - COMPLETE SET
    path('orders/', views.order_list),                    # GET all orders
    path('orders/create/', views.order_create),           # POST new order
    path('orders/<str:order_id>/', views.get_order_details),     # ✅ ADD THIS - GET single order
    path('orders/<str:order_id>/status/', views.update_order_status),  # ✅ ADD THIS - PATCH update status
    
    path('upload/', views.upload),
    path('seed-database/', views.seed_database),
    
    # Authentication
    path('auth/login/', views.login_view, name='login'),
    path('auth/register/', views.register_view, name='register'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/profile/', views.get_profile, name='profile'),
]