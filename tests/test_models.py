from app.models.usuario import Usuario
from app import db


def test_hasheo_contrasena(app):
    with app.app_context():
        usuario = Usuario(nombre="Nuevo", email="nuevo@test.com", rol="estudiante")
        usuario.set_password("secreto123")
        assert usuario.password_hash != "secreto123"
        assert usuario.check_password("secreto123") is True
        assert usuario.check_password("otra") is False


def test_usuario_unique_email(app):
    with app.app_context():
        counts = Usuario.query.filter_by(email="admin@test.com").count()
        assert counts == 1


def test_crear_curso_desde_modelo(app):
    from app.models.curso import Curso

    with app.app_context():
        docente = Usuario.query.filter_by(rol="docente").first()
        curso = Curso(nombre="Curso Nuevo", descripcion="Test", docente_id=docente.id)
        db.session.add(curso)
        db.session.commit()
        assert Curso.query.filter_by(nombre="Curso Nuevo").count() == 1