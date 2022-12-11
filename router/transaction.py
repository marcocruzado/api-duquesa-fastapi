# Python
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

# Get specific transaction by transaction_id
@router.get("/specific_detail/{transaction_id}")
def show_specific_transaction(
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
    sql = "SELECT tt.transaction_id, tt.user_id, tu.name AS user_name, tu.lastname AS user_lastname, tu.msisdn AS user_msisdn, tu.email AS user_email, tt.service_id, ts.name AS service_name, ts.description AS service_description, ts.amount AS service_amount, tt.additional_id, tt.total_amount, tt.registration_timestamp FROM db_duquesa.tb_transaction AS tt INNER JOIN db_duquesa.tb_user AS tu ON tt.user_id = tu.user_id INNER JOIN db_duquesa.tb_service AS ts ON tt.service_id = ts.service_id where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    data = query.fetchone()
    if data == None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "¡This transaction doesn't exist! Enter another transaction_id."
            )
    # Get additional_services
    if data.additional_id != None:
        additional_services = []
        for i in eval(data.additional_id):        
                sql = "select additional_id, name AS additional_name, description AS additional_description, amount AS additional_amount from db_duquesa.tb_additional where additional_id = {}".format(i)
                query = conn.execute(sql)
                data2 = query.fetchall()
                data2 = data2[0]
                additional_services.append(data2)
    else: additional_services = None
    return {
        "message": "Transaction successfully found.",
        "transaction_id": data.transaction_id,
        "user": {
            "user_id": data.user_id,
            "user_name": data.user_name,
            "user_lastname": data.user_lastname,
            "user_msisdn": data.user_msisdn,
            "user_email": data.user_email
        },
        "service": {
            "service_id": data.service_id,
            "service_name": data.service_name,
            "service_description": data.service_description,
            "service_amount": data.service_amount,
            "additional_services": additional_services,
            "total_amount": data.total_amount
        },
        "registration_timestamp": data.registration_timestamp
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
    # Validation additional_id & additional_amount
    if additional_id == None: additional_amount = 0
    elif additional_amount == None:
        additional_id = None
        additional_amount = 0
    else:
        # Check if additional id doesn't exist
        for i in additional_id:
            sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(i)
            query = conn.execute(sql)
            data = query.fetchall()
            if len(data) == 0:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "additional_id {}".format(i) + " doesn't exist! Enter another additional_id."
                    )
    # Insert new transaction
    sql = "insert into db_duquesa.tb_transaction (user_id, service_id, service_amount, additional_amount, total_amount, registration_timestamp"
    if additional_id != None: sql += ", additional_id"
    sql += ") values ({}".format(user_id) + ", {}".format(service_id) + ", {}".format(service_amount) + ", '{}'".format(str(additional_amount)) + ", {}".format(total_amount) + ", '{}'".format(current_date_and_time)
    if additional_id != None: sql += ", '{}'".format(str(additional_id))
    sql += ")"
    query = conn.execute(sql)
    # Get last inserted row
    sql = "select * from db_duquesa.tb_transaction order by transaction_id desc limit 1"
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Transaction successfully created.",
        "data": data
        }

# Update transaction
@router.put("/update/{transaction_id}")
def update_transaction(transaction_id: int, transaction: Transaction = Body(...)):
    # Body keys
    user_id = transaction.user_id
    service_id = transaction.service_id
    additional_id = transaction.additional_id
    service_amount = transaction.service_amount
    additional_amount = transaction.additional_amount
    total_amount = transaction.total_amount
    # Check if transaction id doesn't exist
    sql = "select * from db_duquesa.tb_transaction where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "transaction_id {}".format(transaction_id) + " doesn't exist! Enter another transaction_id."
            )
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
    # Validation additional_id & additional_amount
    if additional_id == None: additional_amount = 0
    elif additional_amount == None:
        additional_id = None
        additional_amount = 0
    else:
        # Check if additional id doesn't exist
        for i in additional_id:
            sql = "select * from db_duquesa.tb_additional where additional_id = {}".format(i)
            query = conn.execute(sql)
            data = query.fetchall()
            if len(data) == 0:
                raise HTTPException(
                    status_code = status.HTTP_400_BAD_REQUEST,
                    detail = "additional_id {}".format(i) + " doesn't exist! Enter another additional_id."
                    )
    # Update transaction
    sql = "update db_duquesa.tb_transaction set user_id = {}".format(user_id) + ", service_id = {}".format(service_id) + ", service_amount = {}".format(service_amount) + ", additional_amount = '{}'".format(str(additional_amount)) + ", total_amount = {}".format(total_amount)
    if additional_id != None: sql += ", additional_id = '{}'".format(str(additional_id))
    sql += " where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    # Get last updated row
    sql = "select * from db_duquesa.tb_transaction where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    data = query.fetchone()
    return {
        "message": "Transaction successfully updated.",
        "data": data
        }
    
# Delete transaction
@router.delete("/delete/{transaction_id}")
def delete_transaction(transaction_id: int):
    # Check if transaction id doesn't exist
    sql = "select * from db_duquesa.tb_transaction where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    data = query.fetchall()
    if len(data) == 0:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "transaction_id {}".format(transaction_id) + " doesn't exist! Enter another transaction_id."
            )
    # Delete transaction
    sql = "delete from db_duquesa.tb_transaction where transaction_id = {}".format(transaction_id)
    query = conn.execute(sql)
    return {
        "message": "Transaction successfully deleted."
        }
        