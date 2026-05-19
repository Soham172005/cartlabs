from django.urls import path

from core.views import product_detail, products

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/products", products),
    path("api/products/<str:product_id>", product_detail),
]
