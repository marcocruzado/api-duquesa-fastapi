# Python
from config.db import conn
from schemas.tb_customer import Customer
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

# An instance of the APIRouter class is created
router = APIRouter()

# Get all customers
@router.get("/detail")
def show_all_customers():
    sql = "select * from db_duquesa.tb_customer"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No hay clientes registrados."
            )
    return {
        "message": "Success",
        "data": data
        }

# Get all active customers
@router.get("/detail_active")
def show_all_active_customers():
    sql = "select * from db_duquesa.tb_customer where status = 1"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No hay clientes activos."
            )
    return {
        "message": "Success",
        "data": data
        }

# Get customer by customer_id
@router.get("/detail/{customer_id}")
def show_customer(
    customer_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "Customer id",
        description = "This is the customer id. It's required.",
        example = 1
        )
    ):
    # Check if the customer_id exists
    sql = "select * from db_duquesa.tb_customer where customer_id = {}".format(customer_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No existe cliente registrado con ese id."
            )
    return {
        "message": "Customer successfully found.",
        "data": data
        }

# Add new customer
@router.post("/new")
def create_customer(customer: Customer = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys    
    name = customer.name
    phone = customer.phone
    if customer.email != None:
        email = customer.email
    else:
        email = ''
    status = 1
    # Check if phone exists
    sql = "select * from db_duquesa.tb_customer where phone = {}".format(phone)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡Phone {}".format(phone) + " already exists! Enter another phone."
            )
    if email.length > 0:
        # Check if email exists - if entered
        sql = "select * from db_duquesa.tb_customer where email = '{}'".format(email)
        query = conn.execute(sql)
        data = query.fetchall()
        if len(data) > 0:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "¡email '{}'".format(email) + " already exists! Enter another email."
                )
    # Insert new customer
    sql = "insert into db_duquesa.tb_customer (name, phone, email, status, registration_timestamp) values ('{}', '{}', '{}', {}, '{}')".format(name, phone, email, status, current_date_and_time)
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_customer where customer_id = (select MAX(customer_id) from db_duquesa.tb_customer)"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Customer added successfully",
        "data": data
    }

# Edit customer by customer_id
@router.put("/update/{customer_id}")
def update_customer(
    customer_id: int = Path(
        ...,
        gt = 0,
        lt = 1000,
        title = "Customer id",
        description = "This is the customer id. It's required.",
        example = 1
        )
    ):
    # Check if the customer_id exists
    sql = "select * from db_duquesa.tb_customer where customer_id = {}".format(customer_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No existe cliente registrado con ese id."
            )
    # Body keys    
    name = customer.name
    phone = customer.phone
    if customer.email != None:
        email = customer.email
    else:
        email = ''
    status = customer.status
    # Check if phone exists and belongs to customer
    sql = "select * from db_duquesa.tb_customer where phone = {}".format(phone)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) > 0:
        if data.customer_id != customer_id:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = "¡Phone {}".format(phone) + " already exists! Enter another phone."
                )
    if email.length > 0:
        # Check if email exists - if entered - and belongs to customer
        sql = "select * from db_duquesa.tb_customer where email = '{}'".format(email)
        query = conn.execute(sql)
        data = query.fetchall()
        if len(data) > 0:
            if data.customer_id != customer_id:
                raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND,
                    detail = "¡email {}".format(email) + " already exists! Enter another email."
                    )
    # Update customer
    sql = "update db_duquesa.tb_customer set name = '{}', phone = '{}', email = '{}', status = {}) where customer_id = {}".format(name, phone, email, status, customer_id)
    query = conn.execute(sql)
    # Get updated row
    sql = "select * from db_duquesa.tb_customer where customer_id = {})".format(customer_id)
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Customer updated successfully",
        "data": data
    }

# Get visits by phone
@router.get("/visits/{phone}")
def show_customer_visits(
    phone: str = Path(
        ...,
        min_length = 10,
        max_length = 30,
        title = "Phone",
        description = "This is the phone. It's required.",
        example = "9999999999"
        )
    ):    
    # Check if the customer_id exists
    sql = "select * from db_duquesa.tb_customer where phone = '{}'".format(phone)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No existe cliente registrado con el número de teléfono ingresado."
            )
    # Check if the customer_id exists
    sql = "select COUNT(transaction_id) as visitas from db_duquesa.tb_transaction where customer_id = {}".format(data.customer_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "El cliente no tiene visitas registradas."
            )
    return {
        "message": "Customer visits successfully found.",
        "data": data
        }