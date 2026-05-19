from django.urls import path

from core.views import cart, clear_cart, remove_item

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/cart", cart),
    path("api/cart/clear", clear_cart),
    path("api/cart/<str:product_id>", remove_item),
]
