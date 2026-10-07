from fastapi import APIRouter, Depends,HTTPException,status
from pydantic import BaseModel #para q la clase usuario vaya y se transforme en json de forma facil. 
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm #1:esta es la clase q se va a encargar la autenticacion(usuario y contra) 2: es la forma en la q se va a enviar al API los criterios de auth

router = APIRouter(prefix="/basicauth",
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"error":"Error encontrado"}})

oauth2 = OAuth2PasswordBearer(tokenUrl="login") #le decimos cual sera la url q se encargara de la autenticacion

class User(BaseModel): #aca no puede ir password, pq ira a traves de la red 
    username: str
    name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str #debemos crearlo, pq sino no podra acceder y mandar su contra

users_db = {
    "Polux" : {
        "username": "Polux_username",
        "name": "Polux",
        "email": "polux@gmail.com",
        "disabled": False,
        "password":"polux" #la contrasena debe estar encriptada, es mala practica
    },
    "Efra_key" : {
            "username": "Efra_username",
            "name": "Efrain",
            "email": "erfain@gmail.com",
            "disabled": True,
            "password":"eflin" #la contrasena debe estar encriptada, es mala practica
        }
}

def search_user_db(username: str): #lo usaremos siempre y cuando el password sea necesario
    if username in users_db:
        return UserDB(**users_db[username]) #es necesario ** para respetar los parametros de creacion, 

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) #es necesario ** para respetar los parametros de creacion

async def current_user(token: str = Depends(oauth2)): #funcion para validar si el access token es correcto y el usuario pueda entrar a ciertas rutas. #El depends sirve para buscar el token dentro de nuestro sistema de autenticacion (/login)
    user = search_user(token) #el token es el username (key)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"}) #es para dar info

    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                    detail="Usuario inactivo")
    
    return user

@router.post("/login") #usamos post, pq obtendremos datos pero tmb enviaremos datos <- AUTENTICACION
async def login(form: OAuth2PasswordRequestForm = Depends()): #haremos que el form, por default Depends() <- osea q la autenticacion a recibir datos pero no dependera de nadie
    user_db = users_db.get(form.username) #busca la key del diccionario, ojo con eso, osea Polux o Efra_key. pq es una logica mal implementada, ya q con efra, el key y el username no son iguales
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario no existe")

    user = search_user_db(form.username) #aca si usamos la funcion search_user_db pq si necesitamos la contrasena. Estamos pasando la key Polux o Efra_key
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El password no es correcto")

    return {"access_token": user.username,"token_type":"bearer"}
    #access_token = es el token que sirve para no estar autenticando a cada rato
    #token_type = es la forma de autenticacion existe bearer, oa2, etc
    
@router.get("/users/me")
async def me(user: User = Depends(current_user)): #esta funcion depende de lo que hagamos en current_user (si esta autenticado o no), no tendremos user si current_user no es capaz de devolver user
    return user
