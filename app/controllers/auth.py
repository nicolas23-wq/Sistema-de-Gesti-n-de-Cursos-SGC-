from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.forms.auth_forms import LoginForm
from app.services import auth_service

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = auth_service.autenticar(form.email.data, form.password.data)
        if usuario:
            login_user(usuario)
            if usuario.rol == "admin":
                return redirect(url_for("admin.dashboard"))
            if usuario.rol == "docente":
                return redirect(url_for("docente.dashboard"))
            return redirect(url_for("estudiante.dashboard"))
        flash("Credenciales invalidas. Verifica tu correo y contrasena.", "error")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesion cerrada correctamente.", "success")
    return redirect(url_for("auth.login"))