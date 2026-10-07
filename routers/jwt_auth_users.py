import os

from dotenv import load_dotenv
from fastapi import APIRouter, Depends,HTTPException,status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext #clase para el contexto de encriptacion
from datetime import datetime,timedelta #1: para la fecha del token, 2: para trabajar con calculos de fecha

ALGORITHM = "HS256"
ACCES_TOKEN_DURATION = 1 #duracion del token 
load_dotenv()
SECRET = os.getenv("JWT_SECRET")
if not SECRET:
    raise RuntimeError("Configura JWT_SECRET en el entorno o en .env")

router = APIRouter(prefix="/jwtauth",
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"error":"Error encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

crypt = CryptContext(schemes=["bcrypt"]) #contexto de encriptacion

class User(BaseModel): 
    username: str
    name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str 


users_db = {
    "Polux" : {
        "username": "Polux",
        "name": "Polux",
        "email": "poluxdelacruz@gmail.com",
        "disabled": False,
        "password":"$2a$12$s8mdqFXRRIx.AnBmzBn46edT2ZgwuzfBSaONvDnjvkQmwZTiJqU86" #lupita
    },
    "Efra" : {
            "username": "Efra_username",
            "name": "Efrain",
            "email": "erfain@gmail.com",
            "disabled": True,
            "password":"$2a$12$AMCAzvIzFMrOjUfcQpYBTuJXBmhyzvJH0mgJ6PwumMsR3fRvWpNza" #eflin
        }
}

def search_user_db(username: str): 
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"}) #es para dar info

    try: 
        username = jwt.decode(token,SECRET,algorithms=ALGORITHM).get("sub")
        if username is None:
            raise exception

    except JWTError: #por si ocurre un error con la decodificacion
        raise exception

    return search_user(username)
    

async def current_user(user: User = Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Usuario inactivo")
    
    return user

@router.post("/login") 
async def login(form: OAuth2PasswordRequestForm = Depends()): 
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no existe")

    user = search_user_db(form.username) 

    if not crypt.verify(form.password, user.password): #crypt.verify() lo que hace es verificar si form.password (lo q manda el user) corresponde con la password hasheada en la bd 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El password no es correcto")

    expire = datetime.utcnow() + timedelta(minutes=ACCES_TOKEN_DURATION) #el token expirara en: el tiempo q se creo el token + 1 minuto

    access_token = {"sub": user.username, "exp": expire} #es el access token, sin hashear


    return {"access_token": jwt.encode(access_token,SECRET, algorithm= ALGORITHM), "token_type":"bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)): #esta funcion depende de lo que hagamos en current_user (si esta autenticado o no), no tendremos user si current_user no es capaz de devolver user
    return user
