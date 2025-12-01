from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# carrgenado as variáveis de ambiente
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')

# criando a aplicação
app = FastAPI()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# importando os roteadores
from routes.auth_routes import auth_router
from routes.library_routes import library_router

# incluindo as rotas
app.include_router(auth_router)
app.include_router(library_router)


# para rodar o nosso código, executar no terminal: uvicorn main:app --reload