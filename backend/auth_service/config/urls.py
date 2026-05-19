from django.urls import path

from core.views import login, me, register

urlpatterns = [
    path("health", lambda request: __import__("django.http").http.JsonResponse({"status": "ok"})),
    path("api/auth/register", register),
    path("api/auth/login", login),
    path("api/auth/me", me),
]
