import json
from decimal import Decimal

from django.http import JsonResponse


class CartLabsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


def json_body(request):
    if not request.body:
        return {}
    return json.loads(request.body.decode("utf-8"))


def ok(payload=None, status=200):
    return JsonResponse(payload or {}, status=status, encoder=CartLabsEncoder, safe=not isinstance(payload, list))


def cors(response):
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


def with_cors(view):
    def wrapped(request, *args, **kwargs):
        if request.method == "OPTIONS":
            return cors(JsonResponse({}))
        return cors(view(request, *args, **kwargs))

    return wrapped
