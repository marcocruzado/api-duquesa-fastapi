# Python
from config.db import conn
from schemas.tb_user import User, Login
from datetime import datetime
from auth.verification import hash_password, verify_password

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created
router = APIRouter()

# Get all users
@router.get("/detail")
def show_all_users():
    sql = "select * from db_duquesa.tb_user"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No hay usuarios registrados."
            )
    return {
        "message": "Success",
        "data": data
        }

# Get all active users
@router.get("/detail_active")
def show_all_active_users():
    sql = "select * from db_duquesa.tb_user where status = 1"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No hay usuarios activos registrados."
            )
    return {
        "message": "Success",
        "data": data
        }

# Get user by user_id
@router.get("/detail/{user_id}")
def show_user(
    user_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "User id",
        description = "This is the user id. It's required.",
        example = 1
        )
    ):
    # Check if the user_id exists
    sql = "select * from db_duquesa.tb_user where user_id = {}".format(user_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This user doesn't exist! Enter another user_id."
            )
    return {
        "message": "User successfully found.",
        "data": data
        }

# Add new user
@router.post("/new")
def create_user(user: User = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    role_id = user.role_id
    name = user.name
    lastname = user.lastname
    msisdn = user.msisdn
    email = user.email.lower()
    if user.password != None:
        password = user.password    
    astatus = 1
    # Check if role id doesn't exist
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡role_id {}".format(role_id) + " doesn't exist! Enter another role_id."
            )
    # Check if msisdn exists
    sql = "select * from db_duquesa.tb_user where msisdn = {}".format(msisdn)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Ya existe un usuario con número de teléfono '{}'".format(msisdn) + "! Ingrese otro número de teléfono."            
            )
    # Check if email exists
    sql = "select * from db_duquesa.tb_user where email = '{}'".format(email)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Ya existe un usuario con email '{}'".format(email) + "! Ingrese otro email."            
            )
    # Insert new user
    sql = "insert into db_duquesa.tb_user (role_id, name, lastname, msisdn, email, password, registration_timestamp, status) values ({}, '{}', '{}', {}, '{}', '{}', '{}', {})".format(role_id, name, lastname, msisdn, email, hash_password(password), current_date_and_time, astatus)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_user where user_id = (select MAX(user_id) from db_duquesa.tb_user)"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Usuario agregado satisfactoriamente.",
        "data": data
    }

# Update user
@router.put("/update/{user_id}")
def update_user(
    user_id: int = Path(
        ...,
        gt = 0,
        lt = 10000,
        title = "User id",
        description = "This is the user id. It's required.",
        example = 1001
        ),
    user: User = Body(...)
    ):
    # Body keys
    role_id = user.role_id
    name = user.name
    lastname = user.lastname
    msisdn = user.msisdn
    email = user.email.lower()
    astatus = user.status
    # Check if role id doesn't exist
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡role_id {}".format(role_id) + " doesn't exist! Enter another role_id."
            )
    # Check if user_id exists
    sql = "select * from db_duquesa.tb_user where user_id = {}".format(user_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This id doesn't exist! Enter another user_id."
            )
    # Check if msisdn exists
    sql = "select * from db_duquesa.tb_user where msisdn = '{}'".format(msisdn)
    query = conn.execute(sql)
    data = query.fetchone()
    if data != None:
        if data.user_id != user_id:        
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "¡Ya existe un usuario con número de teléfono '{}'".format(msisdn) + "! Ingrese otro número de teléfono."            
                )  
    # Check if email exists
    sql = "select * from db_duquesa.tb_user where email = '{}'".format(email)
    query = conn.execute(sql)
    data = query.fetchone()
    if data != None:
        if data.user_id != user_id:        
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "¡Ya existe un usuario con email '{}'".format(email) + "! Ingrese otro email."            
                )  
    # Update user
    sql = "update db_duquesa.tb_user set role_id = {}, name = '{}', lastname = '{}', msisdn = '{}',  email = '{}', status = {}".format(role_id, name, lastname, msisdn, email, astatus)
    sql += " where user_id = {}".format(user_id)
    query = conn.execute(sql)
    # Get updated row
    sql = "select * from db_duquesa.tb_user where user_id = {}".format(user_id)
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Usuario actualizado satisfactoriamente.",
        "data": data
        }

# Login
@router.post("/login")
def login(login: Login = Body(...)):
    # Body keys
    email = login.email
    password = login.password
    # Check if email doesn't exist
    sql = "select * from db_duquesa.tb_user where email = '{}'".format(email)
    query = conn.execute(sql)
    if not query.rowcount:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Correo incorrecto."
            )
    # Check if password doesn't exist
    data = query.fetchone()
    if data.role_id != 1 or data.status != 1:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No tiene acceso a este portal."
            )
    if not verify_password(password, data.password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "Contraseña incorrecta."
            )
    # Get access to the web application
    return {
        "message": "Bienvenido, '{}".format(data.name) + " {}'".format(data.lastname),
        "data": data
        }