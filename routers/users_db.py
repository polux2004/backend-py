from fastapi import APIRouter, HTTPException, status #<- httpexception para hacer un raise de un status code, status para errores http
from db.models.user import User #importamos la clase User q es el basemodel
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["userdb"],
                   responses={status.HTTP_404_NOT_FOUND: {"error":"Error encontrado"}})


users_list = []

@router.get("", response_model=list[User])
async def users():
    return users_schema(db_client.users.find())

#Path localhost:8000/user/1 <- usamos el path cuando consideramos q es un parametro obligatorio, es decir, q no puede faltar, en este caso el id del usuario
@router.get("/{id}") 
async def user(id: str):
    return search_user("_id", ObjectId(id))


#Query <- se llama mediante: localhost:8000/userquery/?id=1 <- cuando hay parametros opcionales 
@router.get("/") 
async def user(id: str):
    search_user("_id", ObjectId(id)) #usamos bson 


@router.post("", response_model= User ,status_code=201) #post <- para crear un nuevo usuario, y el status code para que lo default (sin errores) sea 201 en vez 200. Responde model es para lo q se espera retornar correctamtente
async def user(user: User):
    if type(search_user("email",user.email)) == User:
        raise HTTPException(status.HTTP_409_CONFLICT,detail='El email ya esta registrado')
    
    user_dict = dict(user) #tenemos que pasar el usuario a diccionario para q lo entienda nuestra bd no relacional (maneja json)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id #aqui usamos mongo, entramos a local, y decidimos crear el schema users y agregar lo q nos manden como peticion. Despues de eso, se puede asignar un id. agregar usuario a bd + poner id

    new_user = user_schema(db_client.users.find_one({"_id":id}))#buscaremos en la bd el id del nuevo usuario q se acaba de agregar arriba. Pero ojo, pq devuelve como json. buscaremos la forma de transforma de json a tipo User con user_schema

    return User(**new_user)


@router.put("/", response_model= User) #<- actualiza un usuario completo (todos sus parametros)
async def user(user: User):

    user_dict = dict(user) 
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({"_id":ObjectId(user.id)}, user_dict)
    except:
        return {"error":"No se ha encontrado el usuario"}

    return search_user("_id",ObjectId(user.id))

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})

    if not found:
        return {"error":"No se ha eliminado el usuario"}


def search_user(field: str, key):
    try:
        user = user_schema(db_client.users.find_one({field: key})) #field sera la key realmente (criterio de busqueda, email o username). y key es la llave q se buscara por la q se quiere buscar (el valor de email o username)
        return User(**user) #devuelve el usuario completo si existe el email
    except:
        return {"error":"No se encontro el usuario"}