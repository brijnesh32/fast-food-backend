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
    path('orders/', views.order_list),
    path('orders/create/', views.order_create),
    path('upload/', views.upload),
]