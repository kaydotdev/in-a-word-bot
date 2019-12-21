from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dal import dbconnection

connection_string = '{base}://{user}:{pw}@{host}:{port}/{db}'.format(
    base=dbconnection.BASE,
    user=dbconnection.USERNAME,
    pw=dbconnection.PASSWORD,
    host=dbconnection.HOST,
    port=dbconnection.PORT,
    db=dbconnection.DATABASE
)

DBEngine = create_engine(connection_string)
Session = sessionmaker(bind=DBEngine)

ModelBase = declarative_base()
session = Session()
