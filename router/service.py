from fastapi import APIRouter
from config.db import conn
from schemas.tb_service import tb_service

router = APIRouter()

# GET ALL SERVICES
@router.get("/")
async def get_service():
    sql = "SELECT * FROM tb_service"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "success",
        "data": data
        }

# GET SERVICE BY ID
@router.get("/{id}")
async def get_service_by_id(id: int):
    # verificar si existe el id
    sql = "select * from tb_service where service_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el servicio con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Servicio encontrado", 
        "data": data 
        }
        

# ADD NEW SERVICE
@router.post("/")
async def add_service(service: tb_service):
    sql = "insert into tb_service (category_id,name,description,amount,registration_timestamp) values ({}, '{}', '{}', {}, '{}')".format(
        service.category_id, service.name, service.description, service.amount, service.registration_timestamp)
    query = conn.execute(sql)
    # obtern la ultima fila insertada
    sql = "select * from tb_service order by service_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Servicio agregado",
        "data": data
        }

# OBTENER TODOS  LOS SERVICIOS DE UNA CATEGORIA 
@router.get("/category/{id}")
async def get_service_by_category(id: int):
    sql = "select * from tb_service where category_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe la categoria con el id {}".format(id),
            "data": []
        }
    data = query.fetchall()
    return {
        "message": "Servicios encontrados",
        "data": data
    }