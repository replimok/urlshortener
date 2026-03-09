from pydantic import BaseModel, HttpUrl


class URLBase(BaseModel):
    original_url: HttpUrl

class URLCreate(URLBase):
    pass

class URLResponse(BaseModel):
    short_id: str

class URLStats(URLBase):
    short_id: str
    clicks: int

    class Config:
        from_attributes = True
