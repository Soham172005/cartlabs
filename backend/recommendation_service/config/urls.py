from django.urls import path

from core.views import recommendations

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/recommendations/<str:product_id>", recommendations),
]
