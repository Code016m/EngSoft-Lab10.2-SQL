from catalogo import repository

def obter_livros(termo=None):
    if termo:
        return repository.buscar_livros(termo)
    return repository.listar_livros()

def adicionar_livro(titulo, autor, genero, ano):
    if not titulo.strip() or not autor.strip() or not genero.strip() or not ano:
        raise ValueError("Preencha todos os campos.")
    try:
        ano = int(ano)
        if ano <= 0:
            raise ValueError
    except ValueError:
        raise ValueError("Informe um ano válido.")
    livro = {
        "titulo": titulo.strip(),
        "autor": autor.strip(),
        "genero": genero.strip(),
        "ano": ano
    }
    return repository.cadastrar_livro(livro)

def preparar_catalogo():
    repository.inicializar_livros()
