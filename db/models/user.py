from pydantic import BaseModel #para definir un modelo de datos(entidad), para definir la estructura de los datos que vamos a recibir y enviar

class User(BaseModel): #para definir la estructura de los datos que vamos a recibir y enviar, hara que sea mas facil trabajar con los datos, ya q nos permite validar los datos que recibimos y enviamos
    id: str | None = None #no deberia el usuario ingresar su propio id, ya que eso lo generamos nosotros o mongodb
    username: str
    email: str
