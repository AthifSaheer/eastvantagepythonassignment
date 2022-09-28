from sqlalchemy import Column, Integer, String
from db_sqlite import Base

# Table of the address(sqlite)
class AddressBook(Base):
    __tablename__ = "address book"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    postcode = Column(Integer)
    
    location = Column(String)
    latitude = Column(String)
    longitude = Column(String)
