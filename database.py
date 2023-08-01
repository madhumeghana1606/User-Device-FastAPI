from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQL_ALCHEMY_DATABASE_URL="sqlite:///./devices.db"

engine=create_engine(SQL_ALCHEMY_DATABASE_URL,connect_args={"check_same_thread":False})

SessionLocal=sessionmaker(bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db 
    finally:
        db.close()