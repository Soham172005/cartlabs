from django.db import transaction
from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import json_body, ok, with_cors
from cartlabs_common.jwt import require_auth
from core.models import Order, OrderItem


def serialize(order):
    return {
        "id": order.id,
        "status": order.status,
        "subtotal": order.subtotal,
        "createdAt": order.created_at.isoformat(),
        "shipping": {
            "fullName": order.full_name,
            "email": order.email,
            "phone": order.phone,
            "address": order.address,
            "city": order.city,
            "postalCode": order.postal_code,
        },
        "items": [
            {
                "productId": item.product_id,
                "name": item.name,
                "image": item.image,
                "price": item.price,
                "quantity": item.quantity,
            }
            for item in order.items.all()
        ],
    }


@csrf_exempt
@with_cors
@require_auth
def orders(request):
    user_id = request.user_payload["sub"]
    if request.method == "GET":
        return ok({"orders": [serialize(order) for order in Order.objects.filter(user_id=user_id).order_by("-created_at")]})
    if request.method != "POST":
        return ok({"detail": "Method not allowed."}, status=405)
    data = json_body(request)
    shipping = data.get("shipping", {})
    items = data.get("items", [])
    required = ["fullName", "email", "phone", "address", "city", "postalCode"]
    if not items:
        return ok({"detail": "Order requires at least one cart item."}, status=400)
    if any(not shipping.get(field) for field in required):
        return ok({"detail": "All billing and shipping fields are required."}, status=400)
    subtotal = sum(float(item["price"]) * int(item["quantity"]) for item in items)
    with transaction.atomic():
        order = Order.objects.create(
            user_id=user_id,
            full_name=shipping["fullName"],
            email=shipping["email"],
            phone=shipping["phone"],
            address=shipping["address"],
            city=shipping["city"],
            postal_code=shipping["postalCode"],
            subtotal=subtotal,
        )
        OrderItem.objects.bulk_create(
            [
                OrderItem(
                    order=order,
                    product_id=item["productId"],
                    name=item["name"],
                    image=item.get("image", ""),
                    price=item["price"],
                    quantity=item["quantity"],
                )
                for item in items
            ]
        )
    return ok({"order": serialize(Order.objects.prefetch_related("items").get(id=order.id))}, status=201)


@csrf_exempt
@with_cors
@require_auth
def order_detail(request, order_id):
    order = Order.objects.filter(id=order_id, user_id=request.user_payload["sub"]).prefetch_related("items").first()
    if not order:
        return ok({"detail": "Order not found."}, status=404)
    return ok({"order": serialize(order)})
