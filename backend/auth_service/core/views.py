from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt

from cartlabs_common.http import json_body, ok, with_cors
from cartlabs_common.jwt import issue_token, require_auth
from core.models import Customer


def serialize(customer):
    return {"id": customer.id, "fullName": customer.full_name, "email": customer.email}


@csrf_exempt
@with_cors
def register(request):
    if request.method != "POST":
        return ok({"detail": "Method not allowed."}, status=405)
    data = json_body(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    full_name = (data.get("fullName") or "").strip()
    if not full_name or not email or len(password) < 8:
        return ok({"detail": "Full name, valid email and 8+ character password are required."}, status=400)
    if Customer.objects.filter(email=email).exists():
        return ok({"detail": "An account already exists for this email."}, status=409)
    customer = Customer.objects.create(full_name=full_name, email=email, password_hash=make_password(password))
    token = issue_token(customer.id, customer.email, customer.full_name)
    return ok({"token": token, "user": serialize(customer)}, status=201)


@csrf_exempt
@with_cors
def login(request):
    if request.method != "POST":
        return ok({"detail": "Method not allowed."}, status=405)
    data = json_body(request)
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    customer = Customer.objects.filter(email=email).first()
    if not customer or not check_password(password, customer.password_hash):
        return ok({"detail": "Invalid email or password."}, status=401)
    token = issue_token(customer.id, customer.email, customer.full_name)
    return ok({"token": token, "user": serialize(customer)})


@csrf_exempt
@with_cors
@require_auth
def me(request):
    customer = Customer.objects.filter(id=request.user_payload["sub"]).first()
    if not customer:
        return ok({"detail": "User not found."}, status=404)
    return ok({"user": serialize(customer)})
