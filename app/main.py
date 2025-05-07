from fastapi import FastAPI
from .database import create_db_and_tables
from .routes import user, plans, subscriptions

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

app.include_router(user.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
