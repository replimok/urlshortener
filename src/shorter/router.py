from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from src.shorter import utils, models, schemas
from src.database import get_db

router = APIRouter()


@router.post("/shorten", response_model=schemas.URLResponse)
def create_short_id(url_data: schemas.URLCreate, db: Session = Depends(get_db)):
    short_id = utils.generate_short_id(db)
    db_url = models.URL(
        short_id=short_id,
        original_url=str(url_data.original_url)
    )
    db.add(db_url)
    db.commit()

    return schemas.URLResponse(
        short_id=short_id
    )


@router.get("/{short_id}")
def redirect_to_url(short_id: str, db: Session = Depends(get_db)):
    url = db.get(models.URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    url.clicks += 1
    db.commit()

    return RedirectResponse(url=url.original_url, status_code=307)


@router.get("/stats/{short_id}")
def get_stats(short_id: str, db: Session = Depends(get_db)):
    url = db.get(models.URL, short_id)
    if not url:
        raise HTTPException(status_code=404, detail="URL not found")

    return url
