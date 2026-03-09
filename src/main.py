from fastapi import FastAPI
from src.database import engine
from src.shorter import (
    models as shorter_models,
    router as shorter_router
)

shorter_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

app.include_router(shorter_router.router)
