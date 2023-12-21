from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(),name="index"),
    path("conditions", views.Conditions.as_view(),name="conditions"),
    
    path("shop", views.Shop.as_view(),name="shop"),
    path('product/<slug:slug>/', views.ProductDetails.as_view(), name='product_detail'),
    path("wishlist", views.Wishlist.as_view(),name="wishlist"),
    path("error", views.Error.as_view(),name="error"),
    path('chat/', views.ChatAPIView.as_view(), name='chat_api'),
    
]