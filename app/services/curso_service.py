from app import db
from app.models.curso import Curso
from app.models.inscripcion import Inscripcion
from app.models.calificacion import Calificacion
from app.models.usuario import Usuario


def crear_curso(nombre, descripcion, docente_id):
    curso = Curso(nombre=nombre, descripcion=descripcion, docente_id=docente_id)
    db.session.add(curso)
    db.session.commit()
    return curso


def listar_cursos():
    return Curso.query.order_by(Curso.nombre).all()


def buscar_curso(curso_id):
    return db.session.get(Curso, int(curso_id))


def inscribir_estudiante(estudiante_id, curso_id):
    ya_inscrito = Inscripcion.query.filter_by(
        estudiante_id=estudiante_id, curso_id=curso_id
    ).first()
    if ya_inscrito:
        return None, "El estudiante ya esta inscrito en este curso."
    inscripcion = Inscripcion(estudiante_id=estudiante_id, curso_id=curso_id)
    db.session.add(inscripcion)
    db.session.commit()
    return inscripcion, None


def cursos_de_docente(docente_id):
    return Curso.query.filter_by(docente_id=docente_id).order_by(Curso.nombre).all()


def estudiantes_del_curso(curso_id):
    inscripciones = Inscripcion.query.filter_by(curso_id=curso_id).all()
    return [inscripcion.estudiante for inscripcion in inscripciones]


def registrar_calificacion(estudiante_id, curso_id, nota):
    calificacion = Calificacion.query.filter_by(
        estudiante_id=estudiante_id, curso_id=curso_id
    ).first()
    if calificacion:
        calificacion.nota = nota
        mensaje = "Calificacion actualizada."
    else:
        calificacion = Calificacion(
            estudiante_id=estudiante_id, curso_id=curso_id, nota=nota
        )
        db.session.add(calificacion)
        mensaje = "Calificacion registrada."
    db.session.commit()
    return calificacion, mensaje


def cursos_de_estudiante(estudiante_id):
    inscripciones = Inscripcion.query.filter_by(estudiante_id=estudiante_id).all()
    return [inscripcion.curso for inscripcion in inscripciones]


def calificaciones_de_estudiante(estudiante_id):
    return (
        Calificacion.query.filter_by(estudiante_id=estudiante_id)
        .order_by(Calificacion.curso_id)
        .all()
    )