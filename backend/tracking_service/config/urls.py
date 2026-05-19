from django.urls import path

from core.views import tracking

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/tracking/<int:order_id>", tracking),
]
