from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from models import Library, User
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from services import LibraryService, ReaderService
from schemas import LibrarySchema, LoginSchema
from exceptions.library_exception import LibraryAlreadyExistsError
from exceptions.login_exception import LoginError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# cria o token JWT
def _create_token(user_id: int, duration_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token  
    dict_info = {
        'sub': user_id,
        'exp': expiration_date
    }
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

# verifica se o token é válido
def _verify_token(token, session: Session):
    pass

# verifica se o usuário está registrado e se a senha está correta
def _auth_user(user: User | None, password):
    if user and bcrypt_context.verify(password, user.password):
        pass
    else:
        raise LoginError('Usuário não encontrado ou credenciais inválidas!')
        
@auth_router.post('/library')
async def create_library(library_schema: LibrarySchema, session: Session = Depends(get_session)):
    try:
        # cria uma nova biblioteca no banco de dados
        library = Library(**library_schema.model_dump())
        LibraryService.create(session, library)

    except LibraryAlreadyExistsError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception:
        raise HTTPException(status_code=500)

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    
    try:
        if login_schema.admin == False:
            reader = ReaderService.already_registered(session, login_schema.email)
            _auth_user(reader, login_schema.password)
            access_token = _create_token(reader.id)
            refresh_token = _create_token(reader.id, duration_token=timedelta(days=7))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer'
            }
    
    except LoginError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@auth_router.get('/refresh')
async def use_refresh_token(token, session: Session = Depends(get_session)):
    # verificar o token
    user = _verify_token(token)
    access_token = _create_token(user.id)
    return {
                'access_token': access_token,
                'token_type': 'Bearer'
            }
