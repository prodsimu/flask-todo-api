from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request

from .models import User, UserRole


def generate_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
        )
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return {"error": "Token missing"}, 401

        # remove "Bearer " se existir
        if token.startswith("Bearer "):
            token = token[7:]

        try:
            user_id = verify_token(token)
        except ValueError as e:
            return {"error": str(e)}, 401

        return f(user_id=user_id, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(user_id, *args, **kwargs):
        user = User.query.get(user_id)

        if user.role != UserRole.ADMIN.value:
            return {"error": "Admin access required"}, 403

        return f(user_id=user_id, *args, **kwargs)

    return decorated


def self_or_admin_required(f):
    @wraps(f)
    @login_required
    def decorated(user_id, target_user_id, *args, **kwargs):
        current_user = User.query.get(user_id)

        if current_user.role != UserRole.ADMIN.value and user_id != target_user_id:
            return {"error": "Permission denied"}, 403

        return f(user_id=user_id, target_user_id=target_user_id, *args, **kwargs)

    return decorated
