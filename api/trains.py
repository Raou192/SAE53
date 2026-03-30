from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.train import Train
from app.schemas.train import TrainBase

router = APIRouter(prefix="/trains")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/search")
def search_trains(from_: str, to: str, date: str, db: Session = Depends(get_db)):
    trains = db.query(Train).filter(Train.from_station == from_, Train.to_station == to).all()
    return {"results": trains}

@router.get("/{train_id}", response_model=TrainBase)
def get_train(train_id: int, db: Session = Depends(get_db)):
    train = db.query(Train).filter(Train.id == train_id).first()
    if not train:
        raise HTTPException(status_code=404, detail="Train non trouvé")
    return train
