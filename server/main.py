from fastapi import FastAPI
from app.routes import auth as auth_router
from app.db.database import Base, engine

app = FastAPI(title="Black-Channel")

Base.metadata.create_all(bind=engine) #Note

app.include_router(auth_router.router)
