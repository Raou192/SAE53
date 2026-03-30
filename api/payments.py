from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import random

from app.db.session import SessionLocal
from app.models.payment import Payment
from app.models.booking import Booking
from app.core.security import get_current_user
from app.schemas.payment import PaymentCreate, PaymentResponse, PaymentBase

router = APIRouter(prefix="/payments")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("", response_model=PaymentResponse)
def pay(
    payload: PaymentCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    booking = (
        db.query(Booking)
        .filter(Booking.id == payload.bookingId, Booking.user_id == user["sub"])
        .first()
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Réservation introuvable pour cet utilisateur",
        )

    amount = booking.total_price

    status_str = "SUCCESS" if random.random() > 0.2 else "FAILED"

    payment = Payment(
        booking_id=booking.id,
        amount=amount,
        status=status_str,
        created_at=datetime.utcnow().isoformat(),
    )

    db.add(payment)

    if status_str == "SUCCESS":
        booking.status = "CONFIRMED"

    db.commit()
    db.refresh(payment)

    return PaymentResponse(payment=payment)
