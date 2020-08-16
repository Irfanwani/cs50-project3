from django.urls import path

from . import views

app_name = "orders"
urlpatterns = [
    path("", views.index, name="index"),
    path("menu", views.menu, name="menu"),
    path("cart", views.cart, name="cart"),
    path("cart_items", views.cart_items, name="cart_items"),
    path("remove/<int:pizza_id>", views.remove, name="remove"),
    path("removeall", views.removeall, name="removeall"),
    path("order/<int:pizza_id>", views.order, name="order"),
    path("orderall", views.orderall, name="orderall"),
    path("cancelorder/<int:order_id>", views.cancelorder, name="cancelorder"),
    path("checkorders", views.checkorders, name="checkorders"),
    path("updateorder/<str:user>", views.updateorder, name="updateorder")
]
