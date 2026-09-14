from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from app.utils.decorators import role_required
from app.forms.admin_forms import CrearCursoForm, InscribirEstudianteForm, CrearUsuarioForm
from app.services import auth_service, curso_service
from app.models.usuario import Usuario
from app.models.curso import Curso

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/")
@login_required
@role_required("admin")
def dashboard():
    total_cursos = Curso.query.count()
    total_docentes = Usuario.query.filter_by(rol="docente").count()
    total_estudiantes = Usuario.query.filter_by(rol="estudiante").count()
    cursos = curso_service.listar_cursos()
    return render_template(
        "admin/dashboard.html",
        total_cursos=total_cursos,
        total_docentes=total_docentes,
        total_estudiantes=total_estudiantes,
        cursos=cursos,
    )


@admin_bp.route("/cursos")
@login_required
@role_required("admin")
def cursos():
    cursos = curso_service.listar_cursos()
    return render_template("admin/cursos.html", cursos=cursos)


@admin_bp.route("/cursos/crear", methods=["GET", "POST"])
@login_required
@role_required("admin")
def crear_curso():
    form = CrearCursoForm()
    form.docente_id.choices = [
        (docente.id, docente.nombre) for docente in auth_service.obtener_docentes()
    ]
    if form.validate_on_submit():
        curso_service.crear_curso(
            form.nombre.data, form.descripcion.data, form.docente_id.data
        )
        flash("Curso creado exitosamente.", "success")
        return redirect(url_for("admin.cursos"))
    return render_template("admin/crear_curso.html", form=form)


@admin_bp.route("/inscribir", methods=["GET", "POST"])
@login_required
@role_required("admin")
def inscribir():
    form = InscribirEstudianteForm()
    form.curso_id.choices = [
        (curso.id, curso.nombre) for curso in curso_service.listar_cursos()
    ]
    form.estudiante_id.choices = [
        (estudiante.id, estudiante.nombre) for estudiante in auth_service.obtener_estudiantes()
    ]
    if form.validate_on_submit():
        _, error = curso_service.inscribir_estudiante(
            form.estudiante_id.data, form.curso_id.data
        )
        if error:
            flash(error, "error")
        else:
            flash("Estudiante inscrito correctamente.", "success")
        return redirect(url_for("admin.inscribir"))
    return render_template("admin/inscribir.html", form=form)


@admin_bp.route("/usuarios")
@login_required
@role_required("admin")
def usuarios():
    usuarios = auth_service.listar_usuarios()
    return render_template("admin/usuarios.html", usuarios=usuarios)


@admin_bp.route("/usuarios/crear", methods=["GET", "POST"])
@login_required
@role_required("admin")
def crear_usuario():
    form = CrearUsuarioForm()
    if form.validate_on_submit():
        _, error = auth_service.crear_usuario(
            form.nombre.data, form.email.data, form.password.data, form.rol.data
        )
        if error:
            flash(error, "error")
        else:
            flash("Usuario creado exitosamente.", "success")
        return redirect(url_for("admin.usuarios"))
    return render_template("admin/crear_usuario.html", form=form)