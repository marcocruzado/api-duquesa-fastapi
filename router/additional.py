from fastapi import APIRouter
from config.db import conn
from schemas.tb_additional import tb_additional

router = APIRouter()

# GET ALL ADDITIONAL
@router.get("/")
async def get_additional():
    sql = "SELECT * FROM tb_additional"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "success",
        "data": data
        }

# GET ADDITIONAL BY ID
@router.get("/{id}")
async def get_additional_by_id(id: int):
    # verificar si existe el id
    sql = "select * from tb_additional where additional_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el additional con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Additional encontrado", 
        "data": data 
        }

# CREATE ADDITIONAL
@router.post("/")
async def create_additional(additional: tb_additional):
    #verificar si existe el additional
    additional_id = additional.additional_id
    sql = "select * from tb_additional where additional_id = {}".format(additional_id)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "Ya existe el additional con el id {}".format(additional_id),
            "data": []
        }
    # insertar el additional nuevo en la base de datos
    sql = "insert into tb_additional (service_id, name, description, amount, registration_timestamp) values ({}, '{}', '{}', {}, '{}')".format(additional.service_id, additional.name, additional.description, additional.amount, additional.registration_timestamp)
    conn.execute(sql)
    #obtener el ultimo registro insertado
    sql = "SELECT * FROM tb_additional ORDER BY additional_id DESC LIMIT 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Additional creado",
        "data": data
    }

# OBTENER TODOS  LOS ADDITIONAL DE UN SERVICIO
@router.get("/service/{id}")
async def get_additional_by_service(id: int):
    sql = "select * from tb_additional where service_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el servicio con el id {}".format(id),
            "data": []
        }
    data = query.fetchall()
    return {
        "message": "Additional(es) encontrado(s)",
        "data": data
    }