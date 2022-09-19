
from fastapi import APIRouter
from config.db import conn
from schemas.tb_transaction import tb_transaction

router = APIRouter()

# GET ALL TRANSACTIONS
@router.get("/")
async def get_transaction():
    sql = "SELECT * FROM tb_transaction"
    query = conn.execute(sql)
    data = query.fetchall()

    print(data)
    print("MARCO FDP")

    return {
        "message": "success",
        "data": data
        }

# GET TRANSACTION BY ID
@router.get("/{id}")
async def get_transaction_by_id(id: int):
    # verificar si existe el id
    sql = "select * from tb_transaction where transaction_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe la transaccion con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Transaccion encontrada", 
        "data": data 
        }

# ADD NEW TRANSACTION
@router.post("/")
async def add_transaction(transaction: tb_transaction):

    if transaction.additional_amount == []:
        transaction.additional_amount = [0]

    if len(transaction.additional_amount) == 1:
        sql = "insert into tb_transaction (user_id, service_id, service_amount, additional_amount, total_amount,registration_timestamp) values ({}, {}, {}, {}, {},'{}')".format(
            transaction.user_id, transaction.service_id, transaction.service_amount, transaction.additional_amount[0], transaction.total_amount, transaction.registration_timestamp)
        query = conn.execute(sql)
        # obtern la ultima fila insertada
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
            # obtener las ultimas number_rows filas insertadas
            query = conn.execute(
                "select * from tb_transaction order by transaction_id desc limit {}".format(number_rows))
            data = query.fetchall()
        return {
            "message": "Transaccion(es) agregada(s)",
            "data": data
        }
