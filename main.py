from nturl2path import url2pathname
import os
from sys import prefix
from fastapi import FastAPI
from router.transaction import router as transaction_router

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
#rutas para la api de categorias


handler = Mangum(app)