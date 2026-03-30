from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from app.models.booking import Booking
from app.models.train import Train
from app.schemas.booking import BookingWithTrain, BookingList, BookingCreate
from app.schemas.booking import BookingBase
from datetime import datetime

router = APIRouter(prefix="/bookings")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=BookingList)
def my_bookings(user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = user["sub"]
    bookings = db.query(Booking).filter(Booking.user_id == user_id).all()
    return {"bookings": bookings}

@router.get("/{booking_id}", response_model=BookingWithTrain)
def get_booking(booking_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    if booking.user_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé à cette réservation")
    return booking

@router.post("", response_model=BookingBase)
def create_booking(
    payload: BookingCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    train = db.query(Train).filter(Train.id == payload.trainId).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train introuvable")

    unit_price = (
        train.price_first_class
        if payload.travelClass == "first"
        else train.price_second_class
    )

    booking = Booking(
        user_id=user["sub"],
        train_id=payload.trainId,
        departure_date=payload.departureDate,
        travel_class=payload.travelClass,
        passengers_count=payload.passengersCount,
        total_price=unit_price * payload.passengersCount,
        status="PENDING_PAYMENT",
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking

@router.post("/{booking_id}/cancel", response_model=BookingWithTrain)
def cancel_booking(booking_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    if booking.user_id != user["sub"]:
        raise HTTPException(status_code=403, detail="Accès non autorisé à cette réservation")
    booking.status = "CANCELLED"
    db.commit()
    db.refresh(booking)
    return booking
