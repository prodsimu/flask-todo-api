from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import current_app, request

from app.database.database import db
from app.models import User, UserRole


def generate_token(user_id: int):
    payload = {
        "user_id": user_id,
        "exp": datetime.utcnow() + timedelta(hours=3),
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


def _get_token_from_request():
    token = request.headers.get("Authorization")

    if not token:
        return None, ({"error": "Token missing"}, 401)

    if token.startswith("Bearer "):
        token = token[7:]

    return token, None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token, error = _get_token_from_request()

        if error:
            return error

        try:
            user_id = verify_token(token)
        except ValueError as e:
            return {"error": str(e)}, 401

        return f(user_id=user_id, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token, error = _get_token_from_request()

        if error:
            return error

        try:
            user_id = verify_token(token)
        except ValueError as e:
            return {"error": str(e)}, 401

        user = db.session.get(User, user_id)

        if not user or user.role != UserRole.ADMIN.value:
            return {"error": "Admin access required"}, 403

        return f(user_id=user_id, *args, **kwargs)

    return decorated


def self_or_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token, error = _get_token_from_request()

        if error:
            return error

        try:
            user_id = verify_token(token)
        except ValueError as e:
            return {"error": str(e)}, 401

        target_user_id = kwargs.get("target_user_id")
        current_user = db.session.get(User, user_id)

        if not current_user or (
            current_user.role != UserRole.ADMIN.value and user_id != target_user_id
        ):
            return {"error": "Permission denied"}, 403

        return f(user_id=user_id, *args, **kwargs)

    return decorated
