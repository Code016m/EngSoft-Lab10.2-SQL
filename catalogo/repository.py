import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

_client = None
_collection = None

def conectar():
    global _client, _collection

    if _collection is not None:
        return _collection

    host = os.getenv("COSMOS_HOST")
    username = quote_plus(os.getenv("COSMOS_USERNAME", ""))
    password = quote_plus(os.getenv("COSMOS_PASSWORD", ""))

    uri = (
        f"mongodb+srv://{username}:{password}@{host}/"
        "?tls=true&authMechanism=SCRAM-SHA-256"
        "&retrywrites=false&maxIdleTimeMS=120000"
    )
    _client = MongoClient(uri, serverSelectionTimeoutMS=10000)
    _client.admin.command("ping")
    database = _client[os.getenv("COSMOS_DATABASE", "livraria")]
    _collection = database[os.getenv("COSMOS_COLLECTION", "livros")]
    return _collection

def listar_livros():
    collection = conectar()
    return list(collection.find({}, {"_id": 0}).sort("titulo", 1))

def buscar_livros(termo):
    collection = conectar()
    if not termo:
        return listar_livros()
    filtro = {
        "$or": [
            {"titulo": {"$regex": termo, "$options": "i"}},
            {"autor": {"$regex": termo, "$options": "i"}},
            {"genero": {"$regex": termo, "$options": "i"}}
        ]
    }
    return list(collection.find(filtro, {"_id": 0}).sort("titulo", 1))

def cadastrar_livro(livro):
    collection = conectar()
    collection.insert_one(livro)

def inicializar_livros():
    collection = conectar()
    if collection.count_documents({}) == 0:
        livros = [
            {
                "titulo": "Dom Casmurro",
                "autor": "Machado de Assis",
                "genero": "Romance",
                "ano": 1899
            },
            {
                "titulo": "A Hora da Estrela",
                "autor": "Clarice Lispector",
                "genero": "Romance",
                "ano": 1977
            },
            {
                "titulo": "A Moreninha",
                "autor": "Joaquim Manuel de Macedo",
                "genero": "Romance",
                "ano": 1844
            },
            {
                "titulo": "O Cortiço",
                "autor": "Aluísio Azevedo",
                "genero": "Romance",
                "ano": 1890
            },
            {
                "titulo": "Memórias Póstumas de Brás Cubas",
                "autor": "Machado de Assis",
                "genero": "Romance",
                "ano": 1881
            },
            {
                "titulo": "Iracema",
                "autor": "José de Alencar",
                "genero": "Romance",
                "ano": 1865
            },
            {
                "titulo": "Vidas Secas",
                "autor": "Graciliano Ramos",
                "genero": "Romance",
                "ano": 1938
            },
            {
                "titulo": "O Alienista",
                "autor": "Machado de Assis",
                "genero": "Conto",
                "ano": 1882
            },
            {
                "titulo": "Capitães da Areia",
                "autor": "Jorge Amado",
                "genero": "Romance",
                "ano": 1937
            },
            {
                "titulo": "O Guarani",
                "autor": "José de Alencar",
                "genero": "Romance",
                "ano": 1857
            }
        ]
        collection.insert_many(livros)
