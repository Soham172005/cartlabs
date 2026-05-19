import os

import requests
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import cors

ROUTES = {
    "api/auth": os.getenv("AUTH_SERVICE_URL", "http://localhost:8001"),
    "api/products": os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8002"),
    "api/cart": os.getenv("CART_SERVICE_URL", "http://localhost:8003"),
    "api/recommendations": os.getenv("RECOMMENDATION_SERVICE_URL", "http://localhost:8004"),
    "api/orders": os.getenv("ORDER_SERVICE_URL", "http://localhost:8005"),
    "api/tracking": os.getenv("TRACKING_SERVICE_URL", "http://localhost:8006"),
}


@csrf_exempt
def proxy(request, path):
    if request.method == "OPTIONS":
        return cors(JsonResponse({}))
    if path in ("", "health"):
        return cors(JsonResponse({"status": "ok", "service": "cartlabs-gateway"}))
    target_base = next((base for prefix, base in ROUTES.items() if path.startswith(prefix)), None)
    if not target_base:
        return cors(JsonResponse({"detail": "Route not found."}, status=404))
    headers = {"Content-Type": request.headers.get("Content-Type", "application/json")}
    if request.headers.get("Authorization"):
        headers["Authorization"] = request.headers["Authorization"]
    upstream = requests.request(
        method=request.method,
        url=f"{target_base}/{path}",
        params=request.GET,
        data=request.body,
        headers=headers,
        timeout=10,
    )
    response = HttpResponse(upstream.content, status=upstream.status_code, content_type=upstream.headers.get("Content-Type", "application/json"))
    return cors(response)
