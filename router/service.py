# Python
from config.db import conn
from schemas.tb_service import Service
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the FastAPI class is created
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

# Add new service
@router.post("/new")
def create_service(service: Service = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    sql = "insert into db_duquesa.tb_service (category_id, name, description, amount, registration_timestamp) values ({}, '{}', '{}', {}, '{}')".format(service.category_id, service.name, service.description, service.amount, current_date_and_time)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_service order by service_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Service added successfully",
        "data": data
        }