from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.bank_service import create_bank_entry, read_bank_entry, update_bank_entry, delete_bank_entry
from app.models.schemas import BankCreate, BankUpdate, BankResponse
from app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = Config.DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
bank.Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/banks", tags=["banks"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=BankResponse, status_code=status.HTTP_201_CREATED)
def create_bank(bank: BankCreate, db: Session = Depends(get_db)):
    return create_bank_entry(db, bank.name, bank.country)

@router.get("/{bank_id}", response_model=BankResponse)
def read_bank(bank_id: str, db: Session = Depends(get_db)):
    bank = read_bank_entry(db, bank_id)
    if bank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    return bank

@router.put("/{bank_id}", response_model=BankResponse)
def update_bank(bank_id: str, bank: BankUpdate, db: Session = Depends(get_db)):
    updated_bank = update_bank_entry(db, bank_id, bank.dict(exclude_unset=True))
    if updated_bank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    return updated_bank

@router.delete("/{bank_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_bank(bank_id: str, db: Session = Depends(get_db)):
    bank = delete_bank_entry(db, bank_id)
    if bank is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Bank not found")
    return {"detail": "Bank deleted"}
