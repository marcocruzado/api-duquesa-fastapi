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
            detail = "¡There aren't users!"
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
    email = user.email
    password = user.password
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
            detail = "¡msisdn {}".format(msisdn) + " already exists! Enter another msisdn."
            )
    # Check if email exists
    sql = "select * from db_duquesa.tb_user where email = '{}'".format(email)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡email '{}'".format(email) + " already exists! Enter another email."
            )
    # Insert new user
    sql = "insert into db_duquesa.tb_user (role_id, name, lastname, msisdn, email, password, registration_timestamp) values ({}, '{}', '{}', {}, '{}', '{}', '{}')".format(role_id, name, lastname, msisdn, email, hash_password(password), current_date_and_time)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_user where user_id = (select MAX(user_id) from db_duquesa.tb_user)"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "User added successfully",
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
            detail = "¡email '{}'".format(email) + " doesn't exist! Enter another email."
            )
    # Check if password doesn't exist
    data = query.fetchone()
    if not verify_password(password, data.password):
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "¡password '{}'".format(password) + " doesn't exist! Enter correct password."
            )
    # Get access to the web application
    return {
        "message": "Welcome, '{}".format(data.name) + " {}'".format(data.lastname),
        "data": data
        }