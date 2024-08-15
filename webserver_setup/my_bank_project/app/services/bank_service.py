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
