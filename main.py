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

# Initialize Nominatim API
geolocator = Nominatim(user_agent="AddressBookApp")

class AddressBook(BaseModel):
    first_name: str = Field(min_length=1)
    last_name: str = Field(min_length=1)
    postcode: int = Field()
    location: str = Field(min_length=1, max_length=100)

# Just listing all address
@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.AddressBook).all()

# Address adding to the database 
@app.post("/add/address")
def create_address(address: AddressBook, db: Session = Depends(get_db)):

    # saving user-provided data into the database after validation
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

# Address modification API
@app.put("/{address_id}")
def update_address(address_id: int, address: AddressBook, db: Session = Depends(get_db)):
    # collect the address instances that are available in the database
    address_model = db.query(models.AddressBook).filter(models.AddressBook.id == address_id).first()

    #  Raising a 404 error if the address is not available
    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    # if the address is available then update the address with user-provided data
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

# Address deleting API
@app.delete("/{address_id}")
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    # collect the address instances that are available in the database
    address_model = db.query(models.AddressBook).filter(models.AddressBook.id == address_id).first()

    # Raising a 404 error if the address is not available
    if address_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"ID {address_id} : Does not exist"
        )

    # Delete the address if it is available
    db.query(models.AddressBook).filter(models.AddressBook.id == address_id).delete()
    db.commit()
    return "Address successfully deleted!"

# Retrieving the address under the latitude and longitude within the distance
@app.get("/get/under/distance/{latitude}/{longitude}/{distance}")
def get_under_distance(latitude, longitude, distance, db: Session = Depends(get_db)):
    # Collecting all data then assign to a variable
    address = db.query(models.AddressBook).all()

    data = []
    # Iterating the address and finding the distance of each address
    for add in address:
        coords_1 = (add.latitude, add.longitude)
        coords_2 = (latitude, longitude)
        km = GeoDistance.geodesic(coords_1, coords_2).km

        # If matching provided coordinates to the current coordinates then adding the current coordinates to the new list
        if km < int(distance):
            data.append(add)

    # Returning the new list that contains the coordinates
    return data
