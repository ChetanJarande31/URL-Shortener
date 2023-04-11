# from typing import Optional
from pydantic import BaseModel, validator, Field
import validators
from common.constants import SLUG_LIMIT


class UrlSchema(BaseModel):
    longUrl: str
    customSlugCode: str | None = Field(
        default=None, title="The custom code for short url", max_length=SLUG_LIMIT,
    )

    @validator('longUrl')
    def validate_url(cls, v):
        if not validators.url(v):
            raise ValueError("Long URL is invalid.")
        return v
    
    class Config:
        schema_extra = {
            'examples': [
                {
                    "longUrl": "https://chetan.vercel.app.com",
                    "customSlugCode": "vercel",
                }
            ]
        }

class UrlUpdateSchema(BaseModel):
    longUrl: str = Field(title="Original url for update")
 
