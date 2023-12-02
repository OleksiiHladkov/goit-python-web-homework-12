from fastapi import FastAPI, Path, Query, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from contacts_book.routes import contacts
from contacts_book.database.db import get_db

app = FastAPI()

app.include_router(contacts.router, prefix='/api')


@app.get("/")
def read_root():
    return {"message": "Hello World"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=500, detail="Error connecting to the database")