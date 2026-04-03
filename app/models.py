from datetime import datetime
from enum import Enum

from app.database.database import db


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MemberRole(str, Enum):
    VIEWER = "viewer"
    EDITOR = "editor"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(10), nullable=False, default=UserRole.USER.value)

    projects = db.relationship(
        "Project", back_populates="owner", cascade="all, delete-orphan"
    )
    memberships = db.relationship(
        "ProjectMember", back_populates="user", cascade="all, delete-orphan"
    )


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    owner = db.relationship("User", back_populates="projects")
    tasks = db.relationship(
        "Task", back_populates="project", cascade="all, delete-orphan"
    )
    members = db.relationship(
        "ProjectMember", back_populates="project", cascade="all, delete-orphan"
    )


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(20), nullable=False, default=TaskStatus.TODO.value)
    priority = db.Column(
        db.String(10), nullable=False, default=TaskPriority.MEDIUM.value
    )
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    project = db.relationship("Project", back_populates="tasks")
    history = db.relationship(
        "TaskHistory", back_populates="task", cascade="all, delete-orphan"
    )


class TaskHistory(db.Model):
    __tablename__ = "task_history"

    id = db.Column(db.Integer, primary_key=True)
    field = db.Column(db.String(50), nullable=False)
    old_value = db.Column(db.String(255), nullable=True)
    new_value = db.Column(db.String(255), nullable=True)
    changed_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    changed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"), nullable=False)
    task = db.relationship("Task", back_populates="history")


class ProjectMember(db.Model):
    __tablename__ = "project_members"

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False, default=MemberRole.VIEWER.value)
    joined_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)

    user = db.relationship("User", back_populates="memberships")
    project = db.relationship("Project", back_populates="members")

    __table_args__ = (
        db.UniqueConstraint("user_id", "project_id", name="unique_member_per_project"),
    )
