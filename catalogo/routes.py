from flask import Blueprint, render_template, request, redirect, url_for, flash
from catalogo import service
from usuarios import service as usuarios_service
from usuarios import repository as usuarios_repository

catalogo_bp = Blueprint("catalogo", __name__)

@catalogo_bp.route("/", methods=["GET"])
def index():
    termo = request.args.get("busca", "").strip()
    livros = []
    usuarios = []

    try:
        livros = service.buscar_livros(termo)
    except Exception as erro:
        flash(f"Erro ao acessar o catálogo: {erro}", "erro")

    try:
        usuarios_repository.inicializar_usuarios()
        usuarios = usuarios_service.listar_usuarios()
    except Exception as erro:
        flash(f"Erro ao acessar os usuários: {erro}", "erro")

    return render_template(
        "index.html",
        livros=livros,
        usuarios=usuarios,
        termo=termo
    )

@catalogo_bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    try:
        service.cadastrar_livro(
            request.form.get("titulo", ""),
            request.form.get("autor", ""),
            request.form.get("genero", ""),
            request.form.get("ano", "")
        )
        flash("Livro cadastrado com sucesso!", "sucesso")

    except Exception as erro:
        flash(str(erro), "erro")

    return redirect(url_for("catalogo.index"))
