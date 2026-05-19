import os
from datetime import datetime, timedelta, timezone

import jwt
from django.http import JsonResponse

JWT_SECRET = os.getenv("JWT_SECRET", "change-me-in-production")
JWT_ALGORITHM = "HS256"


def issue_token(user_id, email, name):
    payload = {
        "sub": str(user_id),
        "email": email,
        "name": name,
        "iat": datetime.now(timezone.utc),
        "exp": datetime.now(timezone.utc) + timedelta(hours=12),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(request):
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    try:
        return jwt.decode(header.removeprefix("Bearer "), JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None


def require_auth(view):
    def wrapped(request, *args, **kwargs):
        user = decode_token(request)
        if not user:
            return JsonResponse({"detail": "Authentication required."}, status=401)
        request.user_payload = user
        return view(request, *args, **kwargs)

    return wrapped
