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
from routers import auth_router, libraries_router, books_router, loans_router

# incluindo as rotas
app.include_router(auth_router)
app.include_router(libraries_router)
app.include_router(books_router)
app.include_router(loans_router)

# para rodar o nosso código, executar no terminal: uvicorn main:app --reload

# 9788571646858
# 9788522031450
# 8580575397
