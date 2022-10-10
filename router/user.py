from fastapi import APIRouter
from config.db import conn
from schemas.tb_user import Login , tb_user
from auth.verification import hash_password , verify_password

router = APIRouter()


# LOGIN
@router.post("/login")
async def login(login: Login):
    sql = "SELECT * FROM tb_user WHERE email = '{}'".format(login.email)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el usuario con el email {}".format(login.email),
            "data": []
        }
    data = query.fetchone()
    if not verify_password(login.password, data.password):
        return {
            "message": "Contraseña incorrecta",
            "data": []
        }
    return {
        "message": "Bienvenido {}".format(data.name),
        "data": data
    }

# GET ALL USERS
@router.get("/")
async def get_users():
    sql = "SELECT * FROM tb_user"
    query = conn.execute(sql)
    data = query.fetchall()
    if not query.rowcount:
        return {
            "message": "No hay usuarios registrados",
            "data": []
        }
    return {
        "message": "success",
        "data": data
        }


# GET USER BY ID
@router.get("/{id}")
async def get_user_by_id(id: int):
    # verificar si existe el id
    sql = "SELECT * FROM tb_user WHERE user_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe el usuario con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Usuario encontrado", 
        "data": data 
        }

# ADD NEW USER
@router.post("/")
async def add_user(user: tb_user):
    
    # verificar si existe el email
    sql = "SELECT * FROM tb_user WHERE email = '{}'".format(user.email)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "El email {} ya existe".format(user.email),
            "data": []
        }
    # verificar si existe el msisdn
    sql = "SELECT * FROM tb_user WHERE msisdn = '{}'".format(user.msisdn)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "El msisdn {} ya existe".format(user.msisdn),
            "data": []
        }
    # insertar el usuario
    sql = "INSERT INTO tb_user (role_id, name, lastname, msisdn, email, password,registration_timestamp) VALUES ({}, '{}', '{}', '{}', '{}', '{}', '{}')".format(user.role_id, user.name, user.lastname, user.msisdn, user.email, hash_password(user.password), user.registration_timestamp)
    conn.execute(sql)
    # obtener el ultimo id insertado
    sql = "SELECT * FROM tb_user WHERE user_id = (SELECT MAX(user_id) FROM tb_user)"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Usuario registrado",
        "data": data
    }
