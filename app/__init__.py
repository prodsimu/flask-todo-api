import os

from flask_openapi3 import Info, OpenAPI

from app.database.database import db
from app.database.seeds import seed_admin


def create_app():
    info = Info(title="Task Manager API", version="1.0.0")

    security_schemes = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    app = OpenAPI(
        __name__,
        info=info,
        security_schemes=security_schemes,
    )

    secret_key = os.environ.get("SECRET_KEY")
    if not secret_key:
        raise RuntimeError("SECRET_KEY environment variable is not set.")

    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.member_routes import member_bp
    from app.routes.project_routes import project_bp
    from app.routes.task_routes import task_bp
    from app.routes.user_routes import user_bp

    app.register_api(user_bp)
    app.register_api(project_bp)
    app.register_api(task_bp)
    app.register_api(member_bp)

    with app.app_context():
        db.create_all()
        created = seed_admin()

        if created:
            print("Admin created: username=admin | password=admin123456")

    return app
