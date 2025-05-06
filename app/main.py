from .routes import plans

from fastapi import FastAPI
from .database import create_db_and_tables

app = FastAPI(title="Cloud Service Access Management System")
app.include_router(plans.router)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Cloud Service Access API is running"}
