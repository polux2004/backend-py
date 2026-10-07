from fastapi import APIRouter

router = APIRouter(prefix="/products", #prefix para determinar todos los subfijos de los meotods
                    tags=["products"], #sirve para la documentacion en el swagger, separa de los demas rutas
                   responses={404 : {"error":"No encontrado"}}) #defines la rpta por si algo sale mal

products_list=["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def products():
    return ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/{id}")
async def products(id: int):
    return products_list[id]