from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.services import curso_service

estudiante_bp = Blueprint("estudiante", __name__)


@estudiante_bp.route("/")
@login_required
@role_required("estudiante")
def dashboard():
    cursos = curso_service.cursos_de_estudiante(current_user.id)
    calificaciones = curso_service.calificaciones_de_estudiante(current_user.id)
    promedio = (
        round(sum(cal.nota for cal in calificaciones) / len(calificaciones), 2)
        if calificaciones else 0.0
    )
    return render_template(
        "estudiante/dashboard.html",
        cursos=cursos,
        calificaciones=calificaciones,
        promedio=promedio,
    )


@estudiante_bp.route("/mis-cursos")
@login_required
@role_required("estudiante")
def mis_cursos():
    cursos = curso_service.cursos_de_estudiante(current_user.id)
    return render_template("estudiante/mis_cursos.html", cursos=cursos)


@estudiante_bp.route("/mis-calificaciones")
@login_required
@role_required("estudiante")
def mis_calificaciones():
    calificaciones = curso_service.calificaciones_de_estudiante(current_user.id)
    return render_template("estudiante/mis_calificaciones.html", calificaciones=calificaciones)