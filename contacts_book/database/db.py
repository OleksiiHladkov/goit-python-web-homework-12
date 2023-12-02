from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

import configparser
from pathlib import Path


# config parcer
config = configparser.ConfigParser()

path_to_file = Path(__file__).parent.joinpath("config_db.ini")
config.read(path_to_file)

db_user = config.get("DB", "user")
db_pass = config.get("DB", "pass")
host = config.get("DB", "host")
port = config.get("DB", "port")
db_name = config.get("DB", "db_name")


# sql connection
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_pass}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()