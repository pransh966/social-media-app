from dbm import error

import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

#sqlalchemy_database_url = 'postgresql://<<username>>:<<password>>@<ip-address/hostname>:<port>/<database_name>'
sqlalchemy_database_url = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine=create_engine(sqlalchemy_database_url, echo=True)

SessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#while True:
#   try:
#       conn=psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='Saibaba@009',cursor_factory=RealDictCursor)
#        cursor=conn.cursor()
#      print("Database connection was successful")
#        break
#   except Exception as error:
#       print("Connection to database failed")
#       print("Error: ", error)
#       time.sleep(2)

