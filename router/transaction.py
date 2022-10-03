# Python
from config.db import conn
from schemas.tb_transaction import tb_transaction

# FastAPI
from fastapi import APIRouter
from fastapi import Path
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
            detail = "¡This transaction doesn't exist!"
            )
    return {
        "message": "Transaction successfully found.",
        "data": data
        }

# ADD NEW TRANSACTION
@router.post("/")
async def add_transaction(transaction: tb_transaction):
    
    """ 
    data = {
        user_id: 1,
        service_id: 1,
        additional_id: [1,2],
        total_amount: 600,
        register_timestamp: datetime.now()
    """
    
    if transaction.additional_amount == []:
        transaction.additional_amount = [0]
    
    if len(transaction.additional_amount) == 1:
        sql = "insert into tb_transaction (user_id, service_id, service_amount, additional_amount, total_amount,registration_timestamp) values ({}, {}, {}, {}, {},'{}')".format(
            transaction.user_id, transaction.service_id, transaction.service_amount, transaction.additional_amount[0], transaction.total_amount, transaction.registration_timestamp)
        query = conn.execute(sql)
        # Obtener la última fila insertada
        sql = "select * from tb_transaction order by transaction_id desc limit 1"
        query = conn.execute(sql)
        data = query.fetchall()
        return {
            "message": "Transaccion agregada",
            "data": data
        }
    
    else:
        for i in range(len(transaction.additional_amount)):
            sql = "insert into tb_transaction (user_id, service_id, service_amount, additional_amount, total_amount,registration_timestamp) values ({}, {}, {}, {}, {},'{}')".format(
                transaction.user_id, transaction.service_id, transaction.service_amount, transaction.additional_amount[i], transaction.total_amount, transaction.registration_timestamp)
            query = conn.execute(sql)
            number_rows = len(transaction.additional_amount)
            # Obtener las últimas number_rows filas insertadas
            query = conn.execute(
                "select * from tb_transaction order by transaction_id desc limit {}".format(number_rows))
            data = query.fetchall()
        return {
            "message": "Transaccion(es) agregada(s)",
            "data": data
        }