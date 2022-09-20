from fastapi import APIRouter
from config.db import conn
from schemas.tb_category import tb_category

router = APIRouter()


# GET ALL CATEGORIES
@router.get("/")
async def get_category():
    sql = "SELECT * FROM tb_category"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "success",
        "data": data
        }

# GET CATEGORY BY ID
@router.get("/{id}")
async def get_category_by_id(id: int):
    # verificar si existe el id
    sql = "select * from tb_category where category_id = {}".format(id)
    query = conn.execute(sql)
    if not query.rowcount:
        return {
            "message": "No existe la categoria con el id {}".format(id),
            "data": []
        }
    data = query.fetchone()
    return { 
        "message": "Categoria encontrada", 
        "data": data 
        }

# CREATE CATEGORY
@router.post("/")
async def create_category(category: tb_category):
    #verificar si existe la categoria
    category_id = category.category_id
    sql = "select * from tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "Ya existe la categoria con el id {}".format(category_id),
            "data": []
        }
    # insertar la categoria nueva en la base de datos
    sql = "insert into tb_category (category_id,name, description) values ({},'{}', '{}')".format(category.category_id,category.name, category.description)
    conn.execute(sql)
    #obtener el ultimo registro insertado
    sql = "SELECT * FROM tb_category ORDER BY category_id DESC LIMIT 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Categoria creada",
        "data": data
    }