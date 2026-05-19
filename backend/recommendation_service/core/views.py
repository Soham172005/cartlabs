from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import ok, with_cors

PRODUCTS = [
    {"id": "cl-aurora-watch", "name": "Aurora X1 Smart Watch", "category": "Wearables", "price": 249.0, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=900&q=80"},
    {"id": "cl-sonicbuds-pro", "name": "SonicBuds Pro", "category": "Audio", "price": 179.0, "image": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=900&q=80"},
    {"id": "cl-nova-laptop", "name": "NovaBook Air 14", "category": "Computing", "price": 1199.0, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&w=900&q=80"},
    {"id": "cl-focus-camera", "name": "FocusFrame 8K Camera", "category": "Creator Gear", "price": 899.0, "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=900&q=80"},
    {"id": "cl-pulse-speaker", "name": "PulseDock Speaker", "category": "Audio", "price": 329.0, "image": "https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=900&q=80"},
    {"id": "cl-vertex-tablet", "name": "Vertex Pro Tablet", "category": "Computing", "price": 749.0, "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?auto=format&fit=crop&w=900&q=80"},
]


@csrf_exempt
@with_cors
def recommendations(request, product_id):
    selected = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if not selected:
        return ok({"recommendations": PRODUCTS[:3]})
    same_category = [item for item in PRODUCTS if item["category"] == selected["category"] and item["id"] != product_id]
    fallback = [item for item in PRODUCTS if item["id"] != product_id and item not in same_category]
    return ok({"recommendations": (same_category + fallback)[:3]})
