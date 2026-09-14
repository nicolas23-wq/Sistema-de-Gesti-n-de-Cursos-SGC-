import pytest
from config import Config
from app import db as _db
from app import create_app


@pytest.fixture(scope="function")
def app():
    class TestConfig(Config):
        TESTING = True
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        WTF_CSRF_ENABLED = False
        SECRET_KEY = "test-secret"

    application = create_app(TestConfig)
    with application.app_context():
        _db.drop_all()
        _db.create_all()
        _seed_test_data()
    yield application


def _seed_test_data():
    from app.models.usuario import Usuario
    from app.models.curso import Curso
    from app.models.inscripcion import Inscripcion
    from app.models.calificacion import Calificacion

    admin = Usuario(nombre="Admin Test", email="admin@test.com", rol="admin")
    admin.set_password("admin123")
    docente = Usuario(nombre="Docente Test", email="docente@test.com", rol="docente")
    docente.set_password("docente123")
    estudiante = Usuario(nombre="Estudiante Test", email="estudiante@test.com", rol="estudiante")
    estudiante.set_password("estudiante123")
    _db.session.add_all([admin, docente, estudiante])
    _db.session.commit()

    curso = Curso(nombre="Curso Test", descripcion="Descripcion", docente_id=docente.id)
    _db.session.add(curso)
    _db.session.commit()

    inscripcion = Inscripcion(estudiante_id=estudiante.id, curso_id=curso.id)
    _db.session.add(inscripcion)
    _db.session.commit()

    calificacion = Calificacion(estudiante_id=estudiante.id, curso_id=curso.id, nota=15.0)
    _db.session.add(calificacion)
    _db.session.commit()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def db(app):
    return _db