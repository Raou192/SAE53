from fastapi import FastAPI
from app.api import trains, bookings, payments

app = FastAPI(title="TrainBooking API")

app.include_router(trains.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
app.include_router(payments.router, prefix="/api")

@app.get("/api/health")
def health():
    return {"status": "ok"}
