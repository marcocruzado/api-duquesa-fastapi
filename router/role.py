# Python
from config.db import conn
from schemas.tb_role import Role
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created 
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
            detail = "¡This role doesn't exist! Enter another role_id."
            )
    return {
        "message": "Role successfully found.",
        "data": data
        }

# Add new role
@router.post("/new")
def create_role(role: Role = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body key
    name = role.name
    # Check if role name exists
    sql = "select * from db_duquesa.tb_role where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Role named '{}'".format(name) + " already exists! Enter another name."
            )
    # Insert new role
    sql = "insert into db_duquesa.tb_role (name, registration_timestamp) values ('{}', '{}')".format(name, current_date_and_time)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_role order by role_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Role added successfully",
        "data": data
        }

# Update role
@router.put("/update/{role_id}")
def update_role(
    role_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "Role id",
        description = "This is the role id. It's required.",
        example = 1
        ),
    role: Role = Body(...)
    ):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body key
    name = role.name
    # Check if role_id exists
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This role doesn't exist! Enter another role_id."
            )
    # Check if role name exists
    sql = "select * from db_duquesa.tb_role where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Role named '{}'".format(name) + " already exists! Enter another name."
            )
    # Update role
    sql = "update db_duquesa.tb_role set name = '{}', registration_timestamp = '{}' where role_id = {}".format(name, current_date_and_time, role_id)
    query = conn.execute(sql)
    # Get last updated row
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Role updated successfully",
        "data": data
        }

# Delete role
@router.delete("/delete/{role_id}")
def delete_role(
    role_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "Role id",
        description = "This is the role id. It's required.",
        example = 1
        )
    ):
    # Check if role_id exists
    sql = "select * from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This role doesn't exist! Enter another role_id."
            )
    # Delete role
    sql = "delete from db_duquesa.tb_role where role_id = {}".format(role_id)
    query = conn.execute(sql)
    return {
        "message": "Role deleted successfully",
        "data": "Role id: {}".format(role_id)
        }