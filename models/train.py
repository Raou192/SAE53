from sqlalchemy import Column, Integer, String, Float
from app.db.base import Base

class Train(Base):
    __tablename__ = "trains"

    id = Column(Integer, primary_key=True, index=True)
    from_station = Column(String, nullable=False)
    to_station = Column(String, nullable=False)
    departure_time = Column(String, nullable=False)
    arrival_time = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    train_type = Column(String, nullable=False)
    price_second_class = Column(Float, nullable=False)
    price_first_class = Column(Float, nullable=False)
    seats_available = Column(Integer, nullable=False)
