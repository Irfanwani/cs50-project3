from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("cart_items", views.cart_items, name="cart_items"),
    path("remove/<str:pizza_id>", views.remove, name="remove"),
    path("removeall", views.removeall, name="removeall"),
]
