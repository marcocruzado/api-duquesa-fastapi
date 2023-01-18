# Python
from config.db import conn
from schemas.tb_category import Category
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created 
router = APIRouter()

# Get all categories
@router.get("/detail")
def show_all_categories():
    sql = "select * from db_duquesa.tb_category"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡There aren't categories!"
            )
    return {
        "message": "Success",
        "data": data
        }

# Get category by category_id
@router.get("/detail/{category_id}")
def show_category(
    category_id: int = Path(
        ...,
        gt = 0,
        lt = 10000,
        title = "Category id",
        description = "This is the category id. It's required.",
        example = 1001
        )
    ):
    # Check if the category_id exists
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This category doesn't exist! Enter another category_id."
            )
    return {
        "message": "Category successfully found.",
        "data": data
        }

# Add new category
@router.post("/new")
def create_category(category: Category = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    name = category.name
    description = category.description
    # Check if category name exists
    sql = "select * from db_duquesa.tb_category where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Category named '{}'".format(name) + " already exists! Enter another name."
            )
    # Insert new category
    sql = "insert into db_duquesa.tb_category (name, registration_timestamp"
    if description != None: sql += ", description"
    sql += ") values ('{}'".format(name) + ", '{}'".format(current_date_and_time)
    if description != None: sql += ", '{}'".format(description)
    sql += ")"
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_category order by category_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Category added successfully",
        "data": data
        }
    

# Update category
@router.put("/update/{category_id}")
def update_category(
    category_id: int = Path(
        ...,
        gt = 0,
        lt = 10000,
        title = "Category id",
        description = "This is the category id. It's required.",
        example = 1001
        ),
    category: Category = Body(...)
    ):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    name = category.name
    description = category.description
    # Check if category_id exists
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This category doesn't exist! Enter another category_id."
            )
    # Check if category name exists
    sql = "select * from db_duquesa.tb_category where name = '{}'".format(name)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Category named '{}'".format(name) + " already exists! Enter another name."
            )
    # Update category
    sql = "update db_duquesa.tb_category set name = '{}', registration_timestamp = '{}'".format(name, current_date_and_time)
    if description != None: sql += ", description = '{}'".format(description)
    sql += " where category_id = {}".format(category_id)
    query = conn.execute(sql)
    # Get last updated row
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Category updated successfully",
        "data": data
        }
""" 
# Delete category
@router.delete("/delete/{category_id}")
def delete_category(
    category_id: int = Path(
        ...,
        gt = 0,
        lt = 10000,
        title = "Category id",
        description = "This is the category id. It's required.",
        example = 1001
        )
    ):
    # Check if category_id exists
    sql = "select * from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This category doesn't exist! Enter another category_id."
            )
    # eliminar los servicios en la tabla tb_service que pertenezcan a la categoría
    sql = "delete from db_duquesa.tb_service where category_id = {}".format(category_id)
    query = conn.execute(sql)
    # Delete category
    sql = "delete from db_duquesa.tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    return {
        "message": "Category deleted successfully",
        "data": data
        } """