# Python
from typing import List
from config.db import conn
from schemas.tb_transaction import Transaction
from datetime import datetime

# FastAPI
from fastapi import APIRouter
from fastapi import Body, Path
from fastapi import HTTPException
from fastapi import status

router = APIRouter()

# Get all transactions
@router.get("/detail")
def show_all_transactions():
    sql = "select * from db_duquesa.tb_transaction"
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡There aren't transactions!"
            )
    return {
        "message": "Success",
        "data": data
        }

# Get transaction by transaction_id
@router.get("/detail/{transaction_id}")
def show_transaction(
    transaction_id: int = Path(
        ...,
        gt = 0,
        lt = 10000000,
        title = "Transaction id",
        description = "This is the transaction id. It's required.",
        example = 1
        )
    ):
    # Check if the transaction_id exists
    sql = "select * from db_duquesa.tb_transaction where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This transaction doesn't exist! Enter another transaction_id."
            )
    return {
        "message": "Transaction successfully found.",
        "data": data
        }

# Add new transaction
@router.post("/new")
def create_transaction(transaction: Transaction = Body(...)):
    # Current date and time
    current_date_and_time = datetime.now()
    # Body keys
    user_id = transaction.user_id
    service_id = transaction.service_id
    additional_id = transaction.additional_id
    service_amount = transaction.service_amount
    additional_amount = transaction.additional_amount
    total_amount = transaction.total_amount
    # Check if user id doesn't exist
    sql = "select * from db_duquesa.tb_user where user_id = {}".format(user_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "user_id {}".format(user_id) + " doesn't exist! Enter another user_id."
            )
    # Check if service id doesn't exist
    sql = "select * from db_duquesa.tb_service where service_id = {}".format(service_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "service_id {}".format(service_id) + " doesn't exist! Enter another service_id."
            )
    #si el additional_id es NULL
    if additional_id == None or additional_amount == None:
        additional_id = 0
        additional_amount = 0
    else:
        # Check if additional id doesn't exist
        for i in additional_id:
            sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(i)
            query = conn.execute(sql)
            data = query.fetchall()
            print("aca esta la cosa",len(data))
            if len(data) == 0:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "additional_id {}".format(i) + " doesn't exist! Enter another additional_id."
                    )
    sql = "insert into db_duquesa.tb_transaction (user_id, service_id, additional_id, service_amount, additional_amount, total_amount, registration_timestamp) values ({}, {}, '{}', {}, '{}', {}, '{}')".format(user_id, service_id, str(additional_id), service_amount, str(additional_amount), total_amount, current_date_and_time)
    conn.execute(sql)
    # obtener el ultimo registro
    sql = "select * from db_duquesa.tb_transaction order by transaction_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Transaction successfully created.",
        "data": data
        }

