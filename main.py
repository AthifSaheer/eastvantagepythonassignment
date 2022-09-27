from fastapi import FastAPI, HTTPException, Depends
from db_sqlite import engine, SessionLocal
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
# from geo import lag_log
import asyncio
import models

from geopy.geocoders import Nominatim

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

geolocator = Nominatim(user_agent="MyApp")

class AddressBook(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    postcode: int = Field()
    location: str = Field(min_length=1, max_length=100)


ADDRESSBOOKS = []


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.AddressBook).all()


@app.post("/add/address")
def create_address(address: AddressBook, db: Session = Depends(get_db)):

    address_model = models.AddressBook()
    address_model.first_name = address.first_name
    address_model.last_name = address.last_name
    address_model.postcode = address.postcode
    address_model.location = address.location

    location = geolocator.geocode(address_model.location)

    # location = lag_log(address_model.location)

    # location = lag_log(address_model.location)
    # asyncio.sleep(1)

    address_model.latitude = location.latitude
    address_model.longitude = location.longitude


    db.add(address_model)
    db.commit()

    return address


# @app.put("/{book_id}")
# def update_book(book_id: int, book: AddressBook, db: Session = Depends(get_db)):

#     book_model = db.query(models.AddressBook).filter(models.AddressBook.id == book_id).first()

#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {book_id} : Does not exist"
#         )

#     book_model.title = book.title
#     book_model.author = book.author
#     book_model.description = book.description
#     book_model.rating = book.rating

#     db.add(book_model)
#     db.commit()

#     return book


# @app.delete("/{book_id}")
# async def delete_book(book_id: int, db: Session = Depends(get_db)):

#     book_model = db.query(models.Books).filter(models.Books.id == book_id).first()

#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {book_id} : Does not exist"
#         )

#     db.query(models.Books).filter(models.Books.id == book_id).delete()

#     db.commit()
