import os
from dotenv import load_dotenv
from sqlalchemy import create_engine,MetaData

# Load environment variables
load_dotenv()

#load variables from .env file
MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_DATABASE= os.getenv('MYSQL_DATABASE')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_PORT = os.getenv('MYSQL_PORT')

URL = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'

#creando el engine
engine = create_engine(URL)
#ejecutando metadatos
metadata = MetaData()
# conectarse a la base de datos
conn = engine.connect()
