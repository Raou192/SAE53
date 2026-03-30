from pydantic import BaseModel

class TrainBase(BaseModel):
    id: int
    from_station: str
    to_station: str
    departure_time: str
    arrival_time: str
    duration_minutes: int
    train_type: str
    price_second_class: float
    price_first_class: float
    seats_available: int

    class Config:
        from_attributes = True
