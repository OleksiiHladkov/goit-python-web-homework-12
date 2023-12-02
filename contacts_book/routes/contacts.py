from typing import List

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from sqlalchemy.orm import Session

from contacts_book.database.db import get_db
from contacts_book.schemas import ContactModel, ContactResponce
from contacts_book.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["Contacts"])


@router.get("/", response_model=List[ContactResponce], name="Read contacts")
async def get_contacts(limit: int = Query(10, le=100), offset: int = 0, search: str|None = None, db: Session = Depends(get_db)):
    return await repository_contacts.get_contacts(limit, offset, search, db)


@router.get("/upcoming_birthdays", name="Upcoming birthdays")
async def get_contact(db: Session = Depends(get_db)):
    return await repository_contacts.get_upcoming_birthdays(db)


@router.get("/{contact_id}", response_model=ContactResponce, name="Read contact")
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!")
    
    return contact


@router.post("/", response_model=ContactResponce, name="Create contact", status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_unique_fields(body, db)
    
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact with such unique fields is exists!")
    
    contact = await repository_contacts.create_contact(body, db)
    
    return contact


@router.put("/{contact_id}", response_model=ContactResponce, name="Read contact")
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact_by_unique_fields(body, db)
    
    if contact and contact.id != contact_id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Contact with such unique fields is exists!")
    
    contact = await repository_contacts.update_contact(body, contact_id, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!")

    return contact


@router.delete("/{contact_id}", name="Delete contact")
async def delete_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db)):
    contact = await repository_contacts.delete_contact(contact_id, db)
    
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found!")

    return contact
