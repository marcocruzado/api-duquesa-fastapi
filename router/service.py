# Python
from config.db import conn
from schemas.tb_service import tb_service

# FastAPI
from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from fastapi import status

router = APIRouter()

# Get all services
@router.get("/detail")
def show_all_services():
    sql = "select * from db_duquesa.tb_service"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡There aren't services!"
            )
    return {
        "message": "Success",
        "data": data
        }

# Get service by service_id
@router.get("/detail/{service_id}")
def show_service(
    service_id: int = Path(
        ...,
        gt = 0,
        lt = 1000000,
        title = "Service id",
        description = "This is the service id. It's required.",
        example = 5
        )
    ):
    # Check if the service_id exists
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This service doesn't exist!"
            )
    return {
        "message": "Service successfully found.",
        "data": data
        }

# Get service(s) by category_id
@router.get("/detail_by_category_id/{category_id}")
def show_services_by_category_id(
    category_id: int = Path(
        ...,
        gt = 0,
        lt = 10000,
        title = "Category id",
        description = "This is the category id. It's required.",
        example = 1001
        )
    ):
    # Check if the category_id exists
    sql = "select * from db_duquesa.tb_service where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Service with category_id {}".format(category_id) + " does not exist!"
            )
    return {
        "message": "Service(s) successfully found.",
        "data": data
    }

# ADD NEW SERVICE
@router.post("/")
async def add_service(service: tb_service):
    sql = "insert into tb_service (category_id,name,description,amount,registration_timestamp) values ({}, '{}', '{}', {}, '{}')".format(
        service.category_id, service.name, service.description, service.amount, service.registration_timestamp)
    query = conn.execute(sql)
    # Obtener la última fila insertada
    sql = "select * from tb_service order by service_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Servicio agregado",
        "data": data
        }