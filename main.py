from nturl2path import url2pathname
import os
from sys import prefix
from fastapi import FastAPI
#importando las rutas
from router.transaction import router as transaction_router
from router.role import router as role_router


from mangum import Mangum

stage = os.environ.get("STAGE", None)
openapi_prefix = f"/{stage}" if stage else "/"


app = FastAPI(
    title="Api Duqueza",
    description="Api para la el salon spa Duqueza",
    version="0.1.0",
    openapi_prefix=openapi_prefix
)



#rutas para la api de transacciones
app.include_router(transaction_router, prefix="/transaction", tags=["Transaction"])
#rutas para la api de roles
app.include_router(role_router, prefix="/role", tags=["Role"])


handler = Mangum(app)