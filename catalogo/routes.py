from flask import Blueprint, render_template, request, redirect, url_for, flash
from catalogo import service

catalogo_bp = Blueprint("catalogo", __name__)


@catalogo_bp.route("/", methods=["GET"])
def index():
    try:
        service.preparar_catalogo()

        termo = request.args.get("busca", "").strip()
        livros = service.obter_livros(termo)

        return render_template(
            "index.html",
            livros=livros,
            busca=termo
        )

    except Exception as erro:
        return render_template(
            "index.html",
            livros=[],
            busca="",
            erro=str(erro)
        )


@catalogo_bp.route("/cadastrar", methods=["POST"])
def cadastrar():
    try:
        service.adicionar_livro(
            request.form.get("titulo", ""),
            request.form.get("autor", ""),
            request.form.get("genero", ""),
            request.form.get("ano", "")
        )

        flash("Livro cadastrado com sucesso!", "sucesso")

    except Exception as erro:
        flash(f"Erro ao cadastrar livro: {erro}", "erro")

    return redirect(url_for("catalogo.index"))
