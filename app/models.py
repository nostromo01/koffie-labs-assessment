from typing import Optional, List
from pydantic import BaseModel, validator
from sqlalchemy import Boolean, Column, String
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

from app.constants import VALID_VIN_REGEX

# Setup in-memory database
SQLALCHEMY_DATABASE_URL = 'sqlite:///vehicles.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, future=True, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """
    Generator to yield database session to SQLite
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class DBVehicle(Base):
    """
    ORM Class for Vehicle
    """
    __tablename__ = 'vehicles'

    vin = Column(String(17), primary_key=True, index=True)
    make = Column(String)
    model = Column(String)
    model_year = Column(String)
    body_class = Column(String)
    cached = Column(Boolean, default=True)


Base.metadata.create_all(bind=engine)


class Vehicle(BaseModel):
    """
    Internal data representation of DB Vehicle row
        Input VIN Requested (string, exactly 17 alphanumeric characters)
        Make (String)
        Model (String)
        Model Year (String)
        Body Class (String)
        Cached Result? (Boolean)
    """
    vin: str
    make: Optional[str]
    model: Optional[str]
    model_year: Optional[str]
    body_class: Optional[str]
    cached: Optional[bool]

    @validator('vin')
    def vin_validator(cls, vin):
        if len(vin) != 17:
            raise ValueError('Invalid VIN submitted, must be 17 characters')
        if not VALID_VIN_REGEX.match(vin):
            raise ValueError('Invalid VIN submitted, must conform to NHTSA VIN format')
        return vin

    class Config:
        orm_mode = True


def get_vehicle(db: Session, vin: str) -> DBVehicle:
    return db.query(DBVehicle).where(DBVehicle.vin == vin).first()


def get_vehicles(db: Session) -> List[DBVehicle]:
    return db.query(DBVehicle).all()


def drop_vehicle(db: Session, vin: str) -> bool:
    if element := db.query(DBVehicle).where(DBVehicle.vin == vin).first():
        db.delete(element)
        db.commit()
        return True
    return False


def create_vehicle(db: Session, vehicle: Vehicle) -> DBVehicle:
    db_vehicle = DBVehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
