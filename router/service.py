# Python
from config.db import conn
from schemas.tb_service import Service
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created 
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
            detail = "¡This service doesn't exist! Enter another service_id."
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
            detail = "¡Service with category_id {}".format(category_id) + " does not exist! Enter another category_id."
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
    # Body keys
    category_id = service.category_id
    name = service.name
    description = service.description
    amount = service.amount
    # Check if category id doesn't exist
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡category_id {}".format(category_id) + " doesn't exist! Enter another category_id."
            )
    # Check if service name exists
    sql = "select * from db_duquesa.tb_service where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Service named '{}'".format(name) + " already exists! Enter another name."
            )
    # Insert new service
    sql = "insert into db_duquesa.tb_service (category_id, name, amount, registration_timestamp"
    if description != None: sql += ", description"
    sql += ") values ({}".format(category_id) + ", '{}'".format(name) + ", {}".format(amount) + ", '{}'".format(current_date_and_time)
    if description != None: sql += ", '{}'".format(description)
    sql += ")"
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_service order by service_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Service added successfully",
        "data": data
        }

# Update service
@router.put("/update/{service_id}")
def update_service(
    service_id: int = Path(
        ...,
        gt = 0,
        lt = 1000000,
        title = "Service id",
        description = "This is the service id. It's required.",
        example = 5
        ),
    service: Service = Body(...)
    ):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    category_id = service.category_id
    name = service.name
    description = service.description
    amount = service.amount
    # Check if service id doesn't exist
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Service id {}".format(service_id) + " doesn't exist! Enter another service_id."
            )
    # Check if category id doesn't exist
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡category_id {}".format(category_id) + " doesn't exist! Enter another category_id."
            )
    # Check if service name exists
    sql = "select * from db_duquesa.tb_service where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchone()
    if data != None:
        if data.service_id != service_id:        
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "¡Ya existe un servicio con nombre '{}'".format(name) + "! Ingrese otro nombre."
                )
    # Update service
    sql = "update db_duquesa.tb_service set category_id = {}".format(category_id) + ", name = '{}'".format(name) + ", amount = {}".format(amount) + ", registration_timestamp = '{}'".format(current_date_and_time)
    if description != None: sql += ", description = '{}'".format(description)
    sql += " where service_id = {}".format(service_id)
    query = conn.execute(sql)
    # Get row data
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Los datos del servicio han sido actualizados satisfactoriamente.",
        "data": data
        }
    
# Delete service
@router.delete("/delete/{service_id}")
def delete_service(
    service_id: int = Path(
        ...,
        gt = 0,
        lt = 1000000,
        title = "Service id",
        description = "This is the service id. It's required.",
        example = 5
        )
    ):
    # Check if service id doesn't exist
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Service id {}".format(service_id) + " doesn't exist! Enter another service_id."
            )
    # Delete service
    sql = "delete from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    return {
        "message": "Service deleted successfully",
        "data": data
        }