from fastapi import APIRouter, Depends
from infrastructure.dependencies import get_session
from models import Library

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.post('/create_library')
async def create_library(name: str, email: str, password: str, cep: str, session = Depends(get_session)):
    library = session.query(Library).filter(Library.email == email).first()
    if library:
        return {'mensagem': 'Já existe um usuário com esse email!'}
    else:
        new_library = Library(name, email, password, cep)
        session.add(new_library)
        session.commit()
        return {'mensagem': 'Usuário cadastrado com sucesso!'}
