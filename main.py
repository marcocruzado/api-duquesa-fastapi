# Python
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# Import modules
from router.transaction import router as transaction_router
from router.role import router as role_router
from router.service import router as service_router
from router.additional import router as additional_router
from router.category import router as category_router
from router.user import router as user_router
from router.customer import router as customer_router

# FastAPI
from fastapi import FastAPI

stage = os.environ.get("STAGE", None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(
    title = "La Duquesa Salón & Spa",
    description = "Desarrollo Backend del proyecto (APIs).",
    version = "1.1.0",
    root_path = openapi_prefix,
)

#middleware para permitir el acceso a la api desde cualquier origen
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#rutas para la api de transacciones
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])
#rutas para la api de roles
app.include_router(role_router, prefix="/role", tags=["Role"])
#rutas para la api de servicios
app.include_router(service_router, prefix="/service", tags=["Service"])
#rutas para la api de adicionales
app.include_router(additional_router, prefix="/additional", tags=["Additional"])
#rutas para la api de categorias
app.include_router(category_router, prefix="/category", tags=["Category"])
#rutas para la api de usuarios
app.include_router(user_router, prefix="/user", tags=["User"])
#rutas para las apis de clientes
app.include_router(customer_router, prefix="/customer", tags=["Customer"])

handler = Mangum(app)