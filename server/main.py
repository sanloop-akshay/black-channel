from fastapi import FastAPI
from app.routes import auth as auth_router
from app.db.database import Base, engine
from app.core.logger import get_logger
logger = get_logger(__name__)

app = FastAPI(title="Black-Channel")

logger.info()
Base.metadata.create_all(bind=engine) #Note

app.include_router(auth_router.router)
