from app import db


class Inscripcion(db.Model):
    __tablename__ = "inscripciones"

    id = db.Column(db.Integer, primary_key=True)
    estudiante_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey("cursos.id"), nullable=False)

    estudiante = db.relationship("Usuario", backref="inscripciones")
    __table_args__ = (db.UniqueConstraint("estudiante_id", "curso_id", name="uq_inscripcion"),)