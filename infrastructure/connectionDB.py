from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

# conexão com o banco de dados
db = create_engine('sqllite:///database.db')

# base do banco de dados
Base = declarative_base()
