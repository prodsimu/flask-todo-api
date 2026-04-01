from app.database.database import db
from app.models import MemberRole, Project, ProjectMember, User


class MemberService:

    @staticmethod
    def _get_project_as_owner(project_id: int, owner_id: int):
        project = db.session.get(Project, project_id)

        if not project:
            raise ValueError("Project not found.")

        if project.owner_id != owner_id:
            raise PermissionError("Only the project owner can manage members.")

        return project

    # CREATE

    @staticmethod
    def add_member(
        project_id: int,
        owner_id: int,
        username: str,
        role: str = MemberRole.VIEWER.value,
    ):
        project = MemberService._get_project_as_owner(project_id, owner_id)

        if role not in [r.value for r in MemberRole]:
            raise ValueError("Invalid role.")

        user = User.query.filter_by(username=username).first()

        if not user:
            raise ValueError("User not found.")

        if user.id == owner_id:
            raise ValueError("You can't add yourself as a member.")

        existing = ProjectMember.query.filter_by(
            project_id=project_id,
            user_id=user.id,
        ).first()

        if existing:
            raise ValueError("User is already a member of this project.")

        member = ProjectMember(
            user_id=user.id,
            project_id=project.id,
            role=role,
        )

        db.session.add(member)
        db.session.commit()

        return member

    # READ

    @staticmethod
    def list_members(project_id: int, requester_id: int):
        project = db.session.get(Project, project_id)

        if not project:
            raise ValueError("Project not found.")

        is_owner = project.owner_id == requester_id
        is_member = ProjectMember.query.filter_by(
            project_id=project_id,
            user_id=requester_id,
        ).first()

        if not is_owner and not is_member:
            raise PermissionError("Access denied.")

        return ProjectMember.query.filter_by(project_id=project_id).all()

    # UPDATE

    @staticmethod
    def update_member_role(
        project_id: int, owner_id: int, target_user_id: int, role: str
    ):
        MemberService._get_project_as_owner(project_id, owner_id)

        if role not in [r.value for r in MemberRole]:
            raise ValueError("Invalid role.")

        member = ProjectMember.query.filter_by(
            project_id=project_id,
            user_id=target_user_id,
        ).first()

        if not member:
            raise ValueError("Member not found.")

        member.role = role
        db.session.commit()

        return member
