# Python
from config.db import conn
from schemas.tb_role import tb_role

# FastAPI
from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from fastapi import status

router = APIRouter()

# Get all roles
@router.get("/detail")
def show_all_roles():
    sql = "select * from db_duquesa.tb_role"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡There aren't roles!"
            )
    return {
        "message": "Success",
        "data": data
        }

# Get role by role_id
@router.get("/detail/{role_id}")
def show_role(
    role_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "Role id",
        description = "This is the role id. It's required.",
        example = 1
        )
    ):
    # Check if the role_id exists
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This role doesn't exist!"
            )
    return {
        "message": "Role successfully found.",
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