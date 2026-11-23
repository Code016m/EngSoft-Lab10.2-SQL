from flask import Blueprint, redirect, url_for, request, flash
from usuarios import service

usuarios_bp = Blueprint("usuarios", __name__)

@usuarios_bp.route("/usuarios/cadastrar", methods=["POST"])
def cadastrar():
    try:
        service.cadastrar_usuario(
            request.form.get("nome", ""),
            request.form.get("email", "")
        )
        flash("Usuário cadastrado com sucesso!", "sucesso")

    except Exception as erro:
        flash(str(erro), "erro")

    return redirect(url_for("catalogo.index"))

@usuarios_bp.route("/usuarios")
def listar():
    try:
        usuarios = service.listar_usuarios()
        return {
            "usuarios": usuarios
        }

    except Exception as erro:
        return {"erro": str(erro)}, 500
