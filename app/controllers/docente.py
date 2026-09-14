from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.forms.docente_forms import CalificacionForm
from app.services import curso_service

docente_bp = Blueprint("docente", __name__)


@docente_bp.route("/")
@login_required
@role_required("docente")
def dashboard():
    cursos = curso_service.cursos_de_docente(current_user.id)
    return render_template("docente/dashboard.html", cursos=cursos)


@docente_bp.route("/mis-cursos")
@login_required
@role_required("docente")
def mis_cursos():
    cursos = curso_service.cursos_de_docente(current_user.id)
    return render_template("docente/mis_cursos.html", cursos=cursos)


@docente_bp.route("/calificar", methods=["GET", "POST"])
@login_required
@role_required("docente")
def calificar():
    form = CalificacionForm()
    cursos = curso_service.cursos_de_docente(current_user.id)
    form.curso_id.choices = [(c.id, c.nombre) for c in cursos]

    estudiantes = []
    if form.curso_id.data:
        estudiantes = curso_service.estudiantes_del_curso(form.curso_id.data)
    elif cursos:
        estudiantes = curso_service.estudiantes_del_curso(cursos[0].id)
    form.estudiante_id.choices = [(e.id, e.nombre) for e in estudiantes]

    if form.validate_on_submit():
        _, mensaje = curso_service.registrar_calificacion(
            form.estudiante_id.data, form.curso_id.data, form.nota.data
        )
        flash(mensaje, "success")
        return redirect(url_for("docente.calificar"))
    return render_template("docente/calificar.html", form=form, cursos=cursos)