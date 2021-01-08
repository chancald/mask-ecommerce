from django.urls import path
from .views import (
    HomeView,
    ProductDetail,
    OrderSummaryView,
    CheckoutView,
    AfterCheckoutView,
    add_to_cart,
    remove_from_cart,
    add_item_quantity,
    remove_item_quantity,
    remove_from_cart_summary,
)

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('order-summary/', OrderSummaryView.as_view(), name="order_summary"),
    path('add-item-quantity/<slug>/', add_item_quantity, name='add_item_quantity'),
    path('remove-item-quantity/<slug>/', remove_item_quantity, name='remove_item_quantity'),
    path('remove-from-cart-summary/<slug>/', remove_from_cart_summary, name='remove_from_cart_summary'),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('product/<slug>/', ProductDetail.as_view(), name="product"),
    path('after-checkout/', AfterCheckoutView.as_view(), name='after_checkout'),
]