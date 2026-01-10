from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from infrastructure.connectionDB import SessionLocal
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from models import User, Library, Reader


# abre e fecha uma sessão no banco de dados
def get_session():
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()

# verifica se o token é válido
def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_session)):
    try: 
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = int(dict_info.get('sub'))
        admin = bool(dict_info.get('admin'))
    except JWTError: 
        raise HTTPException(status_code=401, detail='Acesso negado, verifique a validade do TOKEN!')
    
    if admin == False:
        user = session.query(Reader).where(Reader.id == id_user).first()
    else:
        user = session.query(Library).where(Library.id == id_user).first()

    return user

# pega a biblioteca logada
def get_current_library(user: User = Depends(verify_token)):
    if not isinstance(user, Library):
        raise HTTPException(status_code=401, detail='Acesso negado!')
    
    return user

# pega o leito logado
def get_current_reader(user: User = Depends(verify_token)):
    if not isinstance(user, Reader):
        raise HTTPException(status_code=401, detail='Acesso negado!')
    
    return user
