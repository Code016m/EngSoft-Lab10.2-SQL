import os
from pymongo import MongoClient
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

_client = None

def get_collection():
    global _client
    if _client is None:
        username = quote_plus(os.getenv("COSMOS_USERNAME", ""))
        password = quote_plus(os.getenv("COSMOS_PASSWORD", ""))
        host = os.getenv("COSMOS_HOST", "")
        if not username or not password or not host:
            raise ValueError("Configure as credenciais do Cosmos DB no .env")
        uri = (
            f"mongodb+srv://{username}:{password}@{host}/"
            "?tls=true&authMechanism=SCRAM-SHA-256"
            "&retrywrites=false&maxIdleTimeMS=120000"
        )
        _client = MongoClient(uri, serverSelectionTimeoutMS=10000)
        _client.admin.command("ping")
    database = _client[os.getenv("COSMOS_DATABASE", "livraria")]
    return database[os.getenv("COSMOS_COLLECTION", "livros")]

def listar_livros():
    return list(get_collection().find().sort("titulo", 1))

def buscar_livros(termo):
    return list(get_collection().find({
        "$or": [
            {"titulo": {"$regex": termo, "$options": "i"}},
            {"autor": {"$regex": termo, "$options": "i"}},
            {"genero": {"$regex": termo, "$options": "i"}}
        ]
    }))

def cadastrar_livro(livro):
    return get_collection().insert_one(livro)

def inicializar_livros():
    collection = get_collection()
    if collection.count_documents({}) == 0:
        livros = [
            {"titulo": "Dom Casmurro", "autor": "Machado de Assis", "genero": "Romance", "ano": 1899},
            {"titulo": "O Cortiço", "autor": "Aluísio Azevedo", "genero": "Romance", "ano": 1890},
            {"titulo": "Memórias Póstumas de Brás Cubas", "autor": "Machado de Assis", "genero": "Romance", "ano": 1881},
            {"titulo": "Iracema", "autor": "José de Alencar", "genero": "Romance", "ano": 1865},
            {"titulo": "A Moreninha", "autor": "Joaquim Manuel de Macedo", "genero": "Romance", "ano": 1844},
            {"titulo": "O Alienista", "autor": "Machado de Assis", "genero": "Conto", "ano": 1882},
            {"titulo": "Vidas Secas", "autor": "Graciliano Ramos", "genero": "Romance", "ano": 1938},
            {"titulo": "Capitães da Areia", "autor": "Jorge Amado", "genero": "Romance", "ano": 1937},
            {"titulo": "A Hora da Estrela", "autor": "Clarice Lispector", "genero": "Romance", "ano": 1977},
            {"titulo": "O Guarani", "autor": "José de Alencar", "genero": "Romance", "ano": 1857}
        ]
        collection.insert_many(livros)
