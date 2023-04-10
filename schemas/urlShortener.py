# from typing import Optional
from pydantic import BaseModel, validator, Field
import validators


class UrlSchema(BaseModel):
    longUrl: str
    customCode: str | None = Field(
        default=None, title="The custom code for short url", max_length=8,
    )

    class Config:
        schema_extra = {
            'examples': [
                {
                    "longUrl": "https://chetan.vercel.app.com",
                    "customCode": "vercel",
                }
            ]
        }

    @validator('longUrl')
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Long URL is invalid.")
        return v

# class UrlShorten(BaseModel):
#     user_id: str
#     url: str

# class UrlShortenUpdate(BaseModel):
#     url: str


# class Url(BaseModel):
#     id: str
#     url: str
#     click_count: int
#     qr_code: str
