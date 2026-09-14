from app.models.usuario import Usuario
from app import db

ROLES = ("admin", "docente", "estudiante")

ADMIN_EMAIL = "admin@correo.com"
DOCENTE_EMAIL = "docente@correo.com"
ESTUDIANTE_EMAIL = "estudiante@correo.com"


def autenticar(email, password):
    usuario = Usuario.query.filter_by(email=email).first()
    if usuario and usuario.check_password(password):
        return usuario
    return None


def obtener_docentes():
    return Usuario.query.filter_by(rol="docente").order_by(Usuario.nombre).all()


def obtener_estudiantes():
    return Usuario.query.filter_by(rol="estudiante").order_by(Usuario.nombre).all()


def listar_usuarios():
    return Usuario.query.order_by(Usuario.rol, Usuario.nombre).all()


def crear_usuario(nombre, email, password, rol):
    if rol not in ROLES:
        return None, f"Rol invalido. Debe ser uno de: {', '.join(ROLES)}"
    if Usuario.query.filter_by(email=email).first():
        return None, "Ya existe un usuario con ese correo."
    usuario = Usuario(nombre=nombre, email=email, rol=rol)
    usuario.set_password(password)
    db.session.add(usuario)
    db.session.commit()
    return usuario, None