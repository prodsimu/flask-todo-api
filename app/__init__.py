import os

from flask_openapi3 import Info, OpenAPI

from app.database.database import db
from app.database.seeds import seed_admin


def create_app():
    info = Info(title="Task Manager API", version="1.0.0")
    app = OpenAPI(__name__, info=info)

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is not set.")

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes import member_bp, project_bp, task_bp, user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(member_bp)

    with app.app_context():
        db.create_all()
        created = seed_admin()

        if created:
            print("Admin created: username=admin | password=admin123456")

    return app
