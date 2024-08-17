# app/models/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class BankCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, example="Bank of America")
    country: str = Field(..., min_length=2, max_length=2, regex="^[A-Z]{2}$", example="US")

class BankUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    country: Optional[str] = Field(None, min_length=2, max_length=2, regex="^[A-Z]{2}$")

class BankResponse(BaseModel):
    id: str
    name: str
    country: str
    created_at: str

    class Config:
        orm_mode = True
