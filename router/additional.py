# Python
from config.db import conn
from schemas.tb_additional import tb_additional

# FastAPI
from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from fastapi import status

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
            detail = "¡This additional doesn't exist!"
            )
    return {
        "message": "Additional successfully found.",
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
            detail = "¡Additional with service_id {}".format(service_id) + " does not exist!"
            )
    return {
        "message": "Additional(s) successfully found.",
        "data": data
    }

# CREATE ADDITIONAL
@router.post("/")
async def create_additional(additional: tb_additional):
    # Verificar si existe el additional
    additional_id = additional.additional_id
    sql = "select * from tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "Ya existe el additional con el id {}".format(additional_id),
            "data": []
        }
    # Insertar el additional nuevo en la base de datos
    sql = "insert into tb_additional (service_id, name, description, amount, registration_timestamp) values ({}, '{}', '{}', {}, '{}')".format(additional.service_id, additional.name, additional.description, additional.amount, additional.registration_timestamp)
    conn.execute(sql)
    # Obtener el último registro insertado
    sql = "SELECT * FROM tb_additional ORDER BY additional_id DESC LIMIT 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Additional creado",
        "data": data
    }