from fastapi import APIRouter, Depends, HTTPException
from infrastructure.dependencies import get_session, verify_token
from sqlalchemy.orm import Session
from jose import jwt
from models import Library, User
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from services import LibraryService, ReaderService
from schemas import LibraryCreate, LoginSchema
from exceptions.library_exception import LibraryAlreadyExistsError
from exceptions.login_exception import LoginError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix='/auth', tags=['auth'])

# cria o token JWT
def _create_token(user_id: int, admin: bool = False, duration_token = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration_token  
    dict_info = {
        'sub': str(user_id),
        'admin': admin,
        'exp': expiration_date
    }
    encoded_jwt = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encoded_jwt

# verifica se o usuário está registrado e se a senha está correta
def _auth_user(user: User | None, password):
    if user and bcrypt_context.verify(password, user.password):
        pass
    else:
        raise LoginError('Usuário não encontrado ou credenciais inválidas!')
        
@auth_router.post('/library')
async def create_library(library_schema: LibraryCreate, session: Session = Depends(get_session)):
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
        
        else: 
            library = LibraryService.already_registered(session, login_schema.email)
            _auth_user(library, login_schema.password)
            access_token = _create_token(library.id, library.admin)
            refresh_token = _create_token(library.id, library.admin, duration_token=timedelta(days=7))
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'token_type': 'Bearer'
            }
    
    except LoginError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500)
    
@auth_router.post('/login-form')
async def login_form(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    try:
        reader = ReaderService.already_registered(session, form.username)
        if reader:
            _auth_user(reader, form.password)
            access_token = _create_token(reader.id)
            return {
                'access_token': access_token,
                'token_type': 'Bearer'
            }
        
        library = LibraryService.already_registered(session, form.username)
        if library: 
            _auth_user(library, form.password)
            access_token = _create_token(library.id, library.admin)
            return {
                'access_token': access_token,
                'token_type': 'Bearer'
            }
           
    
    except LoginError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500)

@auth_router.get('/refresh')
async def use_refresh_token(user: User = Depends(verify_token)):
    try:
        # verificar o token
        access_token = _create_token(user.id)
        return {
                    'access_token': access_token,
                    'token_type': 'Bearer'
                }
    
    except LoginError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception:
        raise HTTPException(status_code=500)
