from sqlalchemy import create_engine,MetaData

#creando el engine
engine = create_engine('mysql+pymysql://admin:duquesa2022@18.209.167.96:50001/db_duquesa')
#ejecutando metadatos
metadata = MetaData()
# conectarse a la base de datos
conn = engine.connect()
