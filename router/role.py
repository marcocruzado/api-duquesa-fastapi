from fastapi import APIRouter
from config.db import conn
from schemas.tb_role import tb_role

router = APIRouter()

# GET ALL ROLES
@router.get("/")
async def get_role():
    sql = "SELECT * FROM tb_role"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "success",
        "data": data
        }

# GET ROLE BY ID
@router.get("/{id}")
async def get_role_by_id(id: int):
    # Verificar si existe el id
    sql = "select * from tb_role where role_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el rol con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Rol encontrado", 
        "data": data 
        }

# CREATE ROLE
@router.post("/")
async def create_role(role: tb_role):
    # Verificar si existe el rol
    role_id = role.role_id
    sql = "select * from tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "Ya existe el rol con el id {}".format(role_id),
            "data": []
        }
    # Insertar el rol nuevo en la base de datos
    sql = "insert into tb_role (role_id, role_name) values ({}, '{}')".format(role.role_id, role.name)
    conn.execute(sql)
    # Obtener el último registro insertado
    sql = "SELECT * FROM tb_role ORDER BY role_id DESC LIMIT 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Rol creado",
        "data": data
    }