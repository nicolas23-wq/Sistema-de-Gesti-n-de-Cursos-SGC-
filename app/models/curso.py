from app import db


class Curso(db.Model):
    __tablename__ = "cursos"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    docente_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    docente = db.relationship("Usuario", backref="cursos")
    inscripciones = db.relationship("Inscripcion", backref="curso", lazy="joined")
    calificaciones = db.relationship("Calificacion", backref="curso", lazy="joined")

    @property
    def estudiantes(self):
        return [inscripcion.estudiante for inscripcion in self.inscripciones]

    def __repr__(self):
        return f"<Curso {self.nombre}>"