from typing import List
from datetime import datetime, timedelta

from sqlalchemy import or_
from sqlalchemy.orm import Session

from contacts_book.database.models import Contact
from contacts_book.schemas import ContactModel



async def get_contacts(limit: int, offset: int, search: str|None, db: Session) -> List[Contact]:
    if search:
        return db.query(Contact).filter(or_(Contact.firstname.icontains(search), Contact.lastname.icontains(search), Contact.email.icontains(search))).limit(limit).offset(offset).all()
    
    return db.query(Contact).limit(limit).offset(offset).all()


async def get_contact_by_id(contact_id: int, db: Session) -> Contact|None:
    return db.query(Contact).filter_by(id=contact_id).first()


async def get_contact_by_unique_fields(body: ContactModel, db: Session) -> Contact|None:
    return db.query(Contact).filter(or_(Contact.phone==body.phone, Contact.email==body.email)).first()


async def create_contact(body: ContactModel, db: Session) -> Contact:
    contact = Contact(**body.model_dump())

    db.add(contact)
    db.commit()
    db.refresh(contact)
    
    return contact


async def update_contact(body: ContactModel, contact_id: int, db: Session) -> Contact|None: 
    contact = await get_contact_by_id(contact_id, db)
    
    if contact:
        contact.firstname = body.firstname
        contact.lastname = body.lastname
        contact.phone = body.phone
        contact.email = body.email
        contact.birthday = body.birthday
        contact.description = body.description

        db.commit()

    return contact


async def delete_contact(contact_id: int, db: Session) -> Contact:
    contact = await get_contact_by_id(contact_id, db)
    
    if contact:
        db.delete(contact)
        db.commit()

    return contact


async def get_upcoming_birthdays(db: Session) -> List[Contact]:
    res_contacts = []
    cur_contacts = []

    # get contacts with limit and offset
    limit = 100
    offset = 0
    flag = True
    while flag:
        contacts_db = await get_contacts(limit, offset, None, db)
        if not len(contacts_db):
            flag = False
        cur_contacts.extend(contacts_db)
        offset += limit
    
    # get list of next seven days
    date = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
    list_dates = []
    
    count = 1
    while count <= 7:
        date += timedelta(1)
        # year = 1 for next equalization dates by month and day
        list_dates.append(datetime(1, date.month, date.day))
        count += 1
    
    # equalization dates
    for contact in cur_contacts:
        # year = 1, this is equalization dates by month and day
        if datetime(1, contact.birthday.month, contact.birthday.day) in list_dates:
            res_contacts.append(contact)
    
    return res_contacts
