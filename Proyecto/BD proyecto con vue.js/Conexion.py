from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_BD = "mysql+mysqlconnector://root:0000@localhost:3306/eco_entorno"
create = create_engine(URL_BD)
session = sessionmaker(autocommit=False, autoflush=False, bind=create)
base = declarative_base()

def get_db():
    connection = session()
    try:
        yield connection
    finally:
        connection.close()
