from fastapi import FastAPI
from routers import products, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#Routers
app.include_router(products.router) #para conectar la api general, con el router products
app.include_router(users_db.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)

app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
async def root(): #siempre que llamamos a un servidor, la operacion q ejecutamos debe ser asincrona
    return "hola FastAPI"

@app.get("/url")
async def url():
    return {'url': 'https://www.youtube.com/watch?v=6oL-0TdVy28&list=PLU8oAlHdN5BktAXdEVCLUYzvDyqRQJ2lk&index=1'}
