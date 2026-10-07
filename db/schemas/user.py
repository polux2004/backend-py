def user_schema(user) -> dict: #aca hacemos la conversion de lo q devuelve la bd (json) a nuestra clase modelo (User)
    return {"id": str(user["_id"]), #el id de mongo db es: _id. Aqui estamos devolviendo como user, extrayendo de como nos dieron en la bd(json), extrayendo el valor de su llave _id 
            "username": user["username"], #extraemos la llave username de json y formulamos a User
            "email": user["email"]} #extraemos la llave email de json y formulamos a User

def users_schema(users) -> list:
    return [user_schema(user) for user in users] #cada usuario q nos llega como users lo pasamos a user_schema y lo devolvemosa