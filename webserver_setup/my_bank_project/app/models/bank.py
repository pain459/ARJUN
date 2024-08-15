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
