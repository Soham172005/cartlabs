from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import ok, with_cors
from core.catalog import PRODUCTS


@csrf_exempt
@with_cors
def products(request):
    query = (request.GET.get("q") or "").strip().lower()
    category = (request.GET.get("category") or "").strip().lower()
    results = PRODUCTS
    if query:
        results = [
            product
            for product in results
            if query in product["name"].lower()
            or query in product["description"].lower()
            or query in product["category"].lower()
        ]
    if category and category != "all":
        results = [product for product in results if product["category"].lower() == category]
    return ok({"products": results, "categories": sorted({product["category"] for product in PRODUCTS})})


@csrf_exempt
@with_cors
def product_detail(request, product_id):
    product = next((item for item in PRODUCTS if item["id"] == product_id), None)
    if not product:
        return ok({"detail": "Product not found."}, status=404)
    return ok({"product": product})
