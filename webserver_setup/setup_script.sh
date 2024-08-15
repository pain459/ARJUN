#!/bin/bash

# Create project structure
mkdir -p my_bank_project/app/{routes,models,services,repositories,utils}
mkdir -p my_bank_project/tests

# Create __init__.py files
touch my_bank_project/app/__init__.py
touch my_bank_project/app/routes/__init__.py
touch my_bank_project/app/models/__init__.py
touch my_bank_project/app/services/__init__.py
touch my_bank_project/app/repositories/__init__.py
touch my_bank_project/app/utils/__init__.py
touch my_bank_project/tests/__init__.py

# Create main.py for entry point
cat <<EOL > my_bank_project/app/main.py
from fastapi import FastAPI
from app.routes import bank_routes

app = FastAPI()

app.include_router(bank_routes.router)
EOL

# Create a config.py for configuration
cat <<EOL > my_bank_project/app/config.py
import os

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')
EOL

# Create bank model
cat <<EOL > my_bank_project/app/models/bank.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Bank(Base):
    __tablename__ = 'banks'

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
EOL

# Create bank repository
cat <<EOL > my_bank_project/app/repositories/bank_repository.py
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
EOL

# Create bank service
cat <<EOL > my_bank_project/app/services/bank_service.py
import random
import string
import datetime

from app.repositories.bank_repository import create_bank, get_bank, update_bank, delete_bank
from app.models.bank import Bank

def generate_bank_id(country_shortform: str, bank_name_shortform: str) -> str:
    date_str = datetime.datetime.utcnow().strftime("%Y%m%d")
    random_hex = ''.join(random.choices(string.hexdigits.lower(), k=6))
    return f"{country_shortform.upper()}{bank_name_shortform.upper()}{date_str}{random_hex}"

def create_bank_entry(db, name: str, country: str):
    bank_id = generate_bank_id(country, name[:3])
    new_bank = Bank(id=bank_id, name=name, country=country)
    return create_bank(db, new_bank)

def read_bank_entry(db, bank_id: str):
    return get_bank(db, bank_id)

def update_bank_entry(db, bank_id: str, updated_details: dict):
    return update_bank(db, bank_id, updated_details)

def delete_bank_entry(db, bank_id: str):
    return delete_bank(db, bank_id)
EOL

# Create bank routes
cat <<EOL > my_bank_project/app/routes/bank_routes.py
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
EOL

echo "Project structure created successfully."
