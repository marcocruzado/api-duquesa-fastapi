# Python
import os
from mangum import Mangum
from router.transaction import router as transaction_router
from router.role import router as role_router
from router.service import router as service_router
from router.additional import router as additional_router
from router.category import router as category_router
from router.user import router as user_router

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

# Rutas para el API de transacciones
app.include_router(transaction_router, prefix = "/transaction", tags = ["Transaction"])
# Rutas para el API de roles
app.include_router(role_router, prefix = "/role", tags = ["Role"])
# Rutas para el API de servicios
app.include_router(service_router, prefix = "/service", tags = ["Service"])
# Rutas para el API de adicionales
app.include_router(additional_router, prefix = "/additional", tags = ["Additional"])
# Rutas para el API de categorias
app.include_router(category_router, prefix = "/category", tags = ["Category"])
# Rutas para el API de usuarios
app.include_router(user_router, prefix = "/user", tags = ["User"])

handler = Mangum(app)