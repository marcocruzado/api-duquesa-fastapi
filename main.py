import os
from fastapi import FastAPI

# Import modules
from router.transaction import router as transaction_router
from router.role import router as role_router
from router.service import router as service_router
from router.additional import router as additional_router
from router.category import router as category_router

from mangum import Mangum

stage = os.environ.get("STAGE", None)
openapi_prefix = f"/{stage}" if stage else "/"

app = FastAPI(
    title = "La Duquesa Salón & Spa",
    description = "APIs desarrolladas con Python y FastAPI.",
    version = "0.1.0",
    openapi_prefix = openapi_prefix
    )

# Paths for transaction APIs
app.include_router(transaction_router, prefix = "/transaction", tags = ["Transaction"])
# Paths for role APIs
app.include_router(role_router, prefix = "/role", tags = ["Role"])
# Paths for service APIs
app.include_router(service_router, prefix = "/service", tags = ["Service"])
# Paths for additional service APIs
app.include_router(additional_router, prefix = "/additional", tags = ["Additional"])
# Paths for category APIs
app.include_router(category_router, prefix = "/category", tags = ["Category"])

handler = Mangum(app)