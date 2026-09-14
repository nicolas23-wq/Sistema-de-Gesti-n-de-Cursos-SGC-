from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Debes iniciar sesion para acceder."


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    from app.controllers.auth import auth_bp
    from app.controllers.admin import admin_bp
    from app.controllers.docente import docente_bp
    from app.controllers.estudiante import estudiante_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(docente_bp, url_prefix="/docente")
    app.register_blueprint(estudiante_bp, url_prefix="/estudiante")

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errores/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errores/404.html"), 404

    _seed_data(app)

    return app


def _seed_data(app):
    with app.app_context():
        from app.models.usuario import Usuario
        from app.models.curso import Curso
        from app.models.inscripcion import Inscripcion

        db.create_all()

        if Usuario.query.first() is None:
            admin = Usuario(nombre="Admin General", email="admin@correo.com", rol="admin")
            admin.set_password("admin123")

            docente = Usuario(nombre="Docente Ejemplo", email="docente@correo.com", rol="docente")
            docente.set_password("docente123")

            estudiante = Usuario(nombre="Estudiante Ejemplo", email="estudiante@correo.com", rol="estudiante")
            estudiante.set_password("estudiante123")

            db.session.add_all([admin, docente, estudiante])
            db.session.commit()

            curso1 = Curso(nombre="Matematicas I", descripcion="Curso introductorio de calculo", docente_id=docente.id)
            curso2 = Curso(nombre="Programacion I", descripcion="Fundamentos de programacion en Python", docente_id=docente.id)
            db.session.add_all([curso1, curso2])
            db.session.commit()

            inscripcion = Inscripcion(estudiante_id=estudiante.id, curso_id=curso1.id)
            db.session.add(inscripcion)
            db.session.commit()
