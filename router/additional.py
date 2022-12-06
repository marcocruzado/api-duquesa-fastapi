# Python
from config.db import conn
from schemas.tb_additional import Additional
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created
router = APIRouter()

# Get all additionals
@router.get("/detail")
def show_all_additionals():
    sql = "select * from db_duquesa.tb_additional"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡There aren't additionals!"
            )
    return {
        "message": "Success",
        "data": data
        }

# Get additional by additional_id
@router.get("/detail/{additional_id}")
def show_additional(
    additional_id: int = Path(
        ...,
        gt = 0,
        lt = 100000,
        title = "Additional id",
        description = "This is the additional id. It's required.",
        example = 5
        )
    ):
    # Check if the additional_id exists
    sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This additional doesn't exist! Enter another additional_id."
            )
    return {
        "message": "Additional service successfully found.",
        "data": data
        }

# Get additional(s) by service_id
@router.get("/detail_by_service_id/{service_id}")
def show_additionals_by_service_id(
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
    sql = "select * from db_duquesa.tb_additional where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Additional with service_id {}".format(service_id) + " does not exist! Enter another service_id."
            )
    return {
        "message": "Additional service(s) successfully found.",
        "data": data
        }

# Add new additional
@router.post("/new")
def create_additional(additional: Additional = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    service_id = additional.service_id
    name = additional.name
    description = additional.description
    amount = additional.amount
    # Check if service id doesn't exist
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡service_id {}".format(service_id) + " doesn't exist! Enter another service_id."
            )
    # Check if name of the additional service exists
    sql = "select * from db_duquesa.tb_additional where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Additional service named '{}'".format(name) + " already exists! Enter another name."
            )
    # Insert new additional service
    sql = "insert into db_duquesa.tb_additional (service_id, name, amount, registration_timestamp"
    if description != None: sql += ", description"
    sql += ") values ({}".format(service_id) + ", '{}'".format(name) + ", {}".format(amount) + ", '{}'".format(current_date_and_time)
    if description != None: sql += ", '{}'".format(description)
    sql += ")"
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_additional order by additional_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Additional service added successfully",
        "data": data
        }

# Update additional
@router.put("/update/{additional_id}")
def update_additional(
    additional_id: int = Path(
        ...,
        gt = 0,
        lt = 100000,
        title = "Additional id",
        description = "This is the additional id. It's required.",
        example = 5
        ),
    additional: Additional = Body(...)
    ):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    service_id = additional.service_id
    name = additional.name
    description = additional.description
    amount = additional.amount
    # Check if additional_id exists
    sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Additional with additional_id {}".format(additional_id) + " does not exist! Enter another additional_id."
            )
    # Check if service id doesn't exist
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡service_id {}".format(service_id) + " doesn't exist! Enter another service_id."
            )
    # Check if name of the additional service exists
    sql = "select * from db_duquesa.tb_additional where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Additional service named '{}'".format(name) + " already exists! Enter another name."
            )
    # Update additional service
    sql = "update db_duquesa.tb_additional set service_id = {}".format(service_id) + ", name = '{}'".format(name) + ", description = '{}'".format(description) + ", amount = {}".format(amount) + ", registration_timestamp = '{}'".format(current_date_and_time) + " where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Additional service updated successfully",
        "data": data
        }


# Delete additional
@router.delete("/delete/{additional_id}")
def delete_additional(
    additional_id: int = Path(
        ...,
        gt = 0,
        lt = 100000,
        title = "Additional id",
        description = "This is the additional id. It's required.",
        example = 5
        )
    ):
    # Check if additional_id exists
    sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Additional with additional_id {}".format(additional_id) + " does not exist! Enter another additional_id."
            )
    # Delete additional service
    sql = "delete from db_duquesa.tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    return {
        "message": "Additional service deleted successfully",
        "data": data
        }