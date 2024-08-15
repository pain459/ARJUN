from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.bank_service import create_bank_entry, read_bank_entry, update_bank_entry, delete_bank_entry
from app.models import bank
from app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bank.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/banks")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_bank(name: str, country: str, db: Session = Depends(get_db)):
    return create_bank_entry(db, name, country)

@router.get("/{bank_id}")
def read_bank(bank_id: str, db: Session = Depends(get_db)):
    bank = read_bank_entry(db, bank_id)
    if bank is None:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank

@router.put("/{bank_id}")
def update_bank(bank_id: str, updated_details: dict, db: Session = Depends(get_db)):
    return update_bank_entry(db, bank_id, updated_details)

@router.delete("/{bank_id}")
def delete_bank(bank_id: str, db: Session = Depends(get_db)):
    bank = delete_bank_entry(db, bank_id)
    if bank is None:
        raise HTTPException(status_code=404, detail="Bank not found")
    return {"detail": "Bank deleted"}
