from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import json_body, ok, with_cors
from cartlabs_common.jwt import require_auth
from core.models import CartItem


def serialize(item):
    return {
        "productId": item.product_id,
        "name": item.name,
        "image": item.image,
        "price": item.price,
        "quantity": item.quantity,
        "lineTotal": item.price * item.quantity,
    }


def cart_summary(user_id):
    items = [serialize(item) for item in CartItem.objects.filter(user_id=user_id).order_by("-updated_at")]
    return {"items": items, "subtotal": sum(item["lineTotal"] for item in items), "count": sum(item["quantity"] for item in items)}


@csrf_exempt
@with_cors
@require_auth
def cart(request):
    user_id = request.user_payload["sub"]
    if request.method == "GET":
        return ok(cart_summary(user_id))
    if request.method != "POST":
        return ok({"detail": "Method not allowed."}, status=405)
    data = json_body(request)
    product_id = data.get("productId")
    if not product_id:
        return ok({"detail": "Product ID is required."}, status=400)
    item, created = CartItem.objects.get_or_create(
        user_id=user_id,
        product_id=product_id,
        defaults={
            "name": data.get("name", "Unknown product"),
            "image": data.get("image", ""),
            "price": data.get("price", 0),
            "quantity": max(int(data.get("quantity", 1)), 1),
        },
    )
    if not created:
        item.quantity += max(int(data.get("quantity", 1)), 1)
        item.save(update_fields=["quantity", "updated_at"])
    return ok(cart_summary(user_id), status=201)


@csrf_exempt
@with_cors
@require_auth
def remove_item(request, product_id):
    if request.method != "DELETE":
        return ok({"detail": "Method not allowed."}, status=405)
    CartItem.objects.filter(user_id=request.user_payload["sub"], product_id=product_id).delete()
    return ok(cart_summary(request.user_payload["sub"]))


@csrf_exempt
@with_cors
@require_auth
def clear_cart(request):
    if request.method != "POST":
        return ok({"detail": "Method not allowed."}, status=405)
    CartItem.objects.filter(user_id=request.user_payload["sub"]).delete()
    return ok(cart_summary(request.user_payload["sub"]))
