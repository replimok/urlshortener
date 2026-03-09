from sqlalchemy import Column, String, Integer
from src.database import Base


class URL(Base):
    __tablename__ = "shorter_urls"

    short_id = Column(String, primary_key=True)
    original_url = Column(String, nullable=False)
    #
    clicks = Column(Integer, default=0)
