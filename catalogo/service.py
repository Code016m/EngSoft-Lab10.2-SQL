from catalogo import repository

def listar_livros():
    return repository.listar_livros()

def buscar_livros(termo):
    return repository.buscar_livros(termo.strip())

def cadastrar_livro(titulo, autor, genero, ano):
    titulo = titulo.strip()
    autor = autor.strip()
    genero = genero.strip()

    if not titulo or not autor or not genero or not ano:
        raise ValueError("Preencha todos os campos do livro.")

    try:
        ano = int(ano)
    except ValueError:
        raise ValueError("O ano deve ser um número inteiro.")

    if ano <= 0:
        raise ValueError("O ano deve ser maior que zero.")

    livro = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "ano": ano
    }

    repository.cadastrar_livro(livro)
