from sqlalchemy.orm import Session
from app.models.bank import Bank

def create_bank(db: Session, bank: Bank):
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank

def get_bank(db: Session, bank_id: str):
    return db.query(Bank).filter(Bank.id == bank_id).first()

def update_bank(db: Session, bank_id: str, updated_bank: dict):
    bank = get_bank(db, bank_id)
    if bank:
        for key, value in updated_bank.items():
            setattr(bank, key, value)
        db.commit()
        db.refresh(bank)
    return bank

def delete_bank(db: Session, bank_id: str):
    bank = get_bank(db, bank_id)
    if bank:
        db.delete(bank)
        db.commit()
    return bank
