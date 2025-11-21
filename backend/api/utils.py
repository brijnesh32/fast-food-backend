import datetime, jwt, os
from functools import wraps
from django.http import JsonResponse
from api.models import User
from werkzeug.security import generate_password_hash, check_password_hash

JWT_SECRET = os.getenv("JWT_SECRET", "jwtsecret")
JWT_ALGO = "HS256"
JWT_EXP = 60 * 60 * 24 * 7

def create_token(user):
    payload = {
        "user_id": str(user.id),
        "email": user.email,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except:
        return None

def auth_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JsonResponse({"detail": "Auth required"}, status=401)
        token = auth.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return JsonResponse({"detail": "Invalid token"}, status=401)
        request.user_payload = payload
        return fn(request, *args, **kwargs)
    return wrapper

hash_password = generate_password_hash
verify_password = check_password_hash
