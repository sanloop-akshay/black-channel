from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.routes import auth as auth_router, socket as socket_router
from app.core.logger import get_logger
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from app.core.settings import storage_uri as uri,settings
from app.db.database import Base 

logger = get_logger(__name__)

limiter = Limiter(key_func=get_remote_address, storage_uri=uri)

app = FastAPI(
    title="Black-Channel",
    docs_url=None,  
    redoc_url=None,  
    openapi_url=None
)

app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)

engine = create_engine(settings.DATABASE_URL, echo=True)  
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router)
app.include_router(socket_router.router)

@app.get("/")
def black_channel():
    return {
        "author"      : "S-A",
        "message"     : "Black Channel's Drop",
        "version"     : "1.0.0",
        "description" : "A Linux Monitor with Secure Socket Channel.",
        "github"      : "https://github.com/sanloop-akshay/black-channel",
        "open-source" : True
        }
    