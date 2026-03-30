from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.train import Train
from app.models.booking import Booking
from app.models.payment import Payment


def create_tables():
    Base.metadata.create_all(bind=engine)


def init_trains(db: Session):
    existing = db.query(Train).count()
    if existing > 0:
        print(f"{existing} trains already present, skipping seed.")
        return

    today = datetime.utcnow().date()

    def iso_dt(hour: int, minute: int = 0):
        dt = datetime.combine(today, datetime.min.time()).replace(
            hour=hour, minute=minute
        )
        return dt.isoformat()

    trains = [
        Train(
            from_station="Paris Gare de Lyon",
            to_station="Lyon Part-Dieu",
            departure_time=iso_dt(8, 0),
            arrival_time=iso_dt(10, 0),
            duration_minutes=120,
            train_type="TGV INOUI",
            price_second_class=49.0,
            price_first_class=89.0,
            seats_available=120,
        ),
        Train(
            from_station="Paris Gare de Lyon",
            to_station="Lyon Part-Dieu",
            departure_time=iso_dt(9, 30),
            arrival_time=iso_dt(11, 45),
            duration_minutes=135,
            train_type="TGV INOUI",
            price_second_class=59.0,
            price_first_class=99.0,
            seats_available=0,
        ),
        Train(
            from_station="Paris Gare de Lyon",
            to_station="Marseille Saint-Charles",
            departure_time=iso_dt(7, 15),
            arrival_time=iso_dt(10, 30),
            duration_minutes=195,
            train_type="TGV INOUI",
            price_second_class=69.0,
            price_first_class=119.0,
            seats_available=80,
        ),
        Train(
            from_station="Lyon Part-Dieu",
            to_station="Marseille Saint-Charles",
            departure_time=iso_dt(14, 0),
            arrival_time=iso_dt(16, 0),
            duration_minutes=120,
            train_type="TGV INOUI",
            price_second_class=39.0,
            price_first_class=79.0,
            seats_available=60,
        ),
        Train(
            from_station="Paris Montparnasse",
            to_station="Rennes",
            departure_time=iso_dt(6, 45),
            arrival_time=iso_dt(8, 15),
            duration_minutes=90,
            train_type="TGV INOUI",
            price_second_class=35.0,
            price_first_class=65.0,
            seats_available=100,
        ),
        Train(
            from_station="Paris Gare du Nord",
            to_station="Lille Europe",
            departure_time=iso_dt(18, 0),
            arrival_time=iso_dt(19, 0),
            duration_minutes=60,
            train_type="TGV INOUI",
            price_second_class=29.0,
            price_first_class=55.0,
            seats_available=50,
        ),
    ]

    db.add_all(trains)
    db.commit()
    print(f"Inserted {len(trains)} trains.")


def main():
    print("Creating tables...")
    create_tables()
    db = SessionLocal()
    try:
        print("Seeding trains...")
        init_trains(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
