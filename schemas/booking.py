from pydantic import BaseModel
from app.schemas.train import TrainBase

class BookingCreate(BaseModel):
    trainId: int
    departureDate: str
    travelClass: str
    passengersCount: int

class BookingBase(BaseModel):
    id: int
    train_id: int
    departure_date: str
    travel_class: str
    passengers_count: int
    total_price: float
    status: str

    class Config:
        from_attributes = True

class BookingWithTrain(BookingBase):
    train: TrainBase

class BookingList(BaseModel):
    bookings: list[BookingWithTrain]
