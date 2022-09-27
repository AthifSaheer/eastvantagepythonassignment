from fastapi import FastAPI, HTTPException, Depends
from db_sqlite import engine, SessionLocal
from pydantic import BaseModel, Field
from geopy.geocoders import Nominatim
import geopy.distance as GeoDistance
from sqlalchemy.orm import Session
import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

geolocator = Nominatim(user_agent="AddressBookApp")

class AddressBook(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    postcode: int = Field()
    location: str = Field(min_length=1, max_length=100)


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
    address_model.latitude = location.latitude
    address_model.longitude = location.longitude

    db.add(address_model)
    db.commit()

    return address


@app.put("/{address_id}")
def update_address(address_id: int, address: AddressBook, db: Session = Depends(get_db)):

    address_model = db.query(models.AddressBook).filter(models.AddressBook.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    address_model.first_name = address.first_name
    address_model.last_name = address.last_name
    address_model.postcode = address.postcode
    address_model.location = address.location

    location = geolocator.geocode(address_model.location)
    address_model.latitude = location.latitude
    address_model.longitude = location.longitude

    db.add(address_model)
    db.commit()

    return address


@app.delete("/{address_id}")
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_model = db.query(models.AddressBook).filter(models.AddressBook.id == address_id).first()

    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    db.query(models.AddressBook).filter(models.AddressBook.id == address_id).delete()
    db.commit()
    return "Address successfully deleted!"

@app.get("/get/under/distance/{location}/{distance}")
def get_under_distance(location, distance, db: Session = Depends(get_db)):
    # address = db.query(models.AddressBook).filter(models.AddressBook.location == location)
    address = db.query(models.AddressBook).all()
    location = geolocator.geocode(location)

    data = []
    for add in address:
        coords_1 = (add.latitude, add.longitude)
        coords_2 = (location.latitude, location.longitude)
        km = GeoDistance.geodesic(coords_1, coords_2).km

        if km < int(distance):
            data.append(add)

    return data