from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list,  name='product_list'),
    path('home/', views.product_list),  # optional alias
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart,   name='add_to_cart'),
    path('cart/',            views.view_cart,         name='view_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('thank-you/', views.thank_you, name='thank_you'),
]
