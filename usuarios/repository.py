import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()

def conectar():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DATABASE", "livraria"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        sslmode="require",
        row_factory=dict_row
    )

def inicializar_tabela():
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(150) UNIQUE NOT NULL
                )
            """)

def listar_usuarios():
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, nome, email
                FROM usuarios
                ORDER BY id
            """)
            return cursor.fetchall()

def buscar_usuario_por_email(email):
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, nome, email
                FROM usuarios
                WHERE email = %s
                """,
                (email,)
            )
            return cursor.fetchone()

def cadastrar_usuario(nome, email):
    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email)
                VALUES (%s, %s)
                RETURNING id, nome, email
                """,
                (nome, email)
            )
            return cursor.fetchone()

def inicializar_usuarios():
    inicializar_tabela()

    usuarios_iniciais = [
        ("Ana Silva", "ana@email.com"),
        ("Bruno Santos", "bruno@email.com"),
        ("Carla Oliveira", "carla@email.com"),
        ("Daniel Souza", "daniel@email.com")
    ]

    with conectar() as conn:
        with conn.cursor() as cursor:
            cursor.executemany(
                """
                INSERT INTO usuarios (nome, email)
                VALUES (%s, %s)
                ON CONFLICT (email) DO NOTHING
                """,
                usuarios_iniciais
            )
