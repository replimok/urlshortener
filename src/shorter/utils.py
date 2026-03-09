import random
import string
from sqlalchemy.orm import Session
from src.shorter.models import URL
from src.config import config


def generate_short_id(db: Session) -> str:
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(random.choices(characters, k=config.SHORT_ID_LENGTH))
        if not db.query(URL).filter(URL.short_id == short_id).first():
            return short_id
