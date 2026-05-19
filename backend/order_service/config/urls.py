from django.urls import path

from core.views import order_detail, orders

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/orders", orders),
    path("api/orders/<int:order_id>", order_detail),
]
