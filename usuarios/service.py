from usuarios import repository

def listar_usuarios():
    return repository.listar_usuarios()

def cadastrar_usuario(nome, email):
    nome = nome.strip()
    email = email.strip().lower()

    if not nome or not email:
        raise ValueError("Preencha todos os campos.")

    if "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Informe um e-mail válido.")

    if repository.buscar_usuario_por_email(email):
        raise ValueError("Este e-mail já está cadastrado.")

    return repository.cadastrar_usuario(nome, email)
