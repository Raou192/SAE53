from pydantic import BaseModel

class PaymentCreate(BaseModel):
    bookingId: int
    cardHolder: str
    cardNumber: str
    expiryMonth: str
    expiryYear: str
    cvc: str

class PaymentBase(BaseModel):
    id: int
    booking_id: int
    amount: float
    status: str
    created_at: str

    class Config:
        from_attributes = True

class PaymentResponse(BaseModel):
    payment: PaymentBase
