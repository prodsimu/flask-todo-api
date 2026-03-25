from flask import Blueprint, jsonify, request

from .services import UserService

user_bp = Blueprint("users", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()

        user = UserService.create_user(
            name=data["name"],
            username=data["username"],
            password=data["password"],
        )

        return jsonify({"id": user.id, "username": user.username}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
