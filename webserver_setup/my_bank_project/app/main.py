from fastapi import FastAPI
from app.routes import bank_routes

app = FastAPI()

app.include_router(bank_routes.router)
