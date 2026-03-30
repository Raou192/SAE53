from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    train_id = Column(Integer, ForeignKey("trains.id"), nullable=False)
    departure_date = Column(String, nullable=False)
    travel_class = Column(String, nullable=False)
    passengers_count = Column(Integer, nullable=False)
    total_price = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="PENDING_PAYMENT")

    train = relationship("Train")
