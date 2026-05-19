from datetime import datetime, timedelta, timezone

from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import ok, with_cors
from cartlabs_common.jwt import require_auth


@csrf_exempt
@with_cors
@require_auth
def tracking(request, order_id):
    now = datetime.now(timezone.utc)
    steps = [
        {"label": "Order placed", "detail": "CartLabs received your order.", "state": "complete", "timestamp": (now - timedelta(hours=4)).isoformat()},
        {"label": "Packed", "detail": "Items are packed and labelled.", "state": "complete", "timestamp": (now - timedelta(hours=2)).isoformat()},
        {"label": "Dispatched", "detail": "Shipment left the fulfillment center.", "state": "active", "timestamp": (now - timedelta(minutes=25)).isoformat()},
        {"label": "In transit", "detail": "Courier scan pending at regional hub.", "state": "pending", "timestamp": None},
        {"label": "Received", "detail": "Delivery confirmation will appear here.", "state": "pending", "timestamp": None},
    ]
    return ok({"orderId": order_id, "carrier": "CartLabs Express", "eta": (now + timedelta(days=3)).date().isoformat(), "steps": steps})
