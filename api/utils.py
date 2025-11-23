import datetime, jwt, os
from functools import wraps
from django.http import JsonResponse
from werkzeug.security import generate_password_hash, check_password_hash
JWT_SECRET = os.getenv('JWT_SECRET', 'jwtsecret')
JWT_ALGO = 'HS256'
JWT_EXP = 60 * 60 * 24 * 7
def create_token(payload):
    p = {
        'user_id': payload.get('user_id'),
        'email': payload.get('email'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXP),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(p, JWT_SECRET, algorithm=JWT_ALGO)
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token
def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
    except jwt.ExpiredSignatureError:
        return {'error': 'token_expired'}
    except Exception:
        return {'error': 'invalid_token'}
def auth_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization') or request.META.get('HTTP_AUTHORIZATION','')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'detail':'Auth required'}, status=401)
        token = auth_header.split(' ',1)[1].strip()
        decoded = decode_token(token)
        if not decoded or 'error' in decoded:
            return JsonResponse({'detail': decoded.get('error','invalid_token')}, status=401)
        request.user_payload = decoded
        return fn(request, *args, **kwargs)
    return wrapper
hash_password = generate_password_hash
verify_password = check_password_hash
