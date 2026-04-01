from flask import Blueprint, jsonify, request

from app.auth import login_required
from app.services.member_service import MemberService

member_bp = Blueprint("members", __name__)


# GET


@member_bp.route("/projects/<int:project_id>/members", methods=["GET"])
@login_required
def list_members(user_id, project_id):
    try:
        members = MemberService.list_members(
            project_id=project_id,
            requester_id=user_id,
        )
        return (
            jsonify(
                [
                    {
                        "id": m.id,
                        "user_id": m.user_id,
                        "username": m.user.username,
                        "role": m.role,
                        "joined_at": m.joined_at.isoformat(),
                    }
                    for m in members
                ]
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 404

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


# POST


@member_bp.route("/projects/<int:project_id>/members", methods=["POST"])
@login_required
def add_member(user_id, project_id):
    data = request.get_json()

    try:
        member = MemberService.add_member(
            project_id=project_id,
            owner_id=user_id,
            username=data.get("username"),
            role=data.get("role", "viewer"),
        )
        return (
            jsonify(
                {
                    "id": member.id,
                    "user_id": member.user_id,
                    "username": member.user.username,
                    "role": member.role,
                    "joined_at": member.joined_at.isoformat(),
                }
            ),
            201,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


# PUT


@member_bp.route(
    "/projects/<int:project_id>/members/<int:target_user_id>", methods=["PUT"]
)
@login_required
def update_member_role(user_id, project_id, target_user_id):
    data = request.get_json()

    try:
        member = MemberService.update_member_role(
            project_id=project_id,
            owner_id=user_id,
            target_user_id=target_user_id,
            role=data.get("role"),
        )
        return (
            jsonify(
                {
                    "id": member.id,
                    "user_id": member.user_id,
                    "username": member.user.username,
                    "role": member.role,
                    "joined_at": member.joined_at.isoformat(),
                }
            ),
            200,
        )

    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


# DELETE
