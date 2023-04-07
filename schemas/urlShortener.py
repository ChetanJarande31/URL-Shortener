from pydantic import BaseModel


class UrlShorten(BaseModel):
    user_id: str
    url: str


class UrlShortenUpdate(BaseModel):
    url: str


class Url(BaseModel):
    id: str
    url: str
    click_count: int
    qr_code: str