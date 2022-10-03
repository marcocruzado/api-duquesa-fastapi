# Python
from config.db import conn
from schemas.tb_category import tb_category

# FastAPI
from fastapi import APIRouter
from fastapi import Path
from fastapi import HTTPException
from fastapi import status

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
            detail = "¡This category doesn't exist!"
            )
    return {
        "message": "Category successfully found.",
        "data": data
        }

# CREATE CATEGORY
@router.post("/")
async def create_category(category: tb_category):
    # Verificar si existe la categoría
    category_id = category.category_id
    sql = "select * from tb_category where category_id = {}".format(category_id)
    query = conn.execute(sql)
    if query.rowcount:
        return {
            "message": "Ya existe la categoria con el id {}".format(category_id),
            "data": []
        }
    # Insertar la categoría nueva en la base de datos
    sql = "insert into tb_category (category_id,name, description) values ({},'{}', '{}')".format(category.category_id,category.name, category.description)
    conn.execute(sql)
    # Obtener el último registro insertado
    sql = "SELECT * FROM tb_category ORDER BY category_id DESC LIMIT 1"
    query = conn.execute(sql)
    data = query.fetchall()
    return {
        "message": "Categoria creada",
        "data": data
    }