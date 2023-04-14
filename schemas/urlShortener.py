# from typing import Optional
from pydantic import BaseModel, validator, Field
import validators
from common.constants import SLUG_LIMIT, USER_ID


class UrlSchema(BaseModel):
    longUrl: str = Field(title="Long url which is to be shorten", example="https://chetan.vercel.app.com")
    customSlugCode: str | None = Field(
        default=None, title="The custom code for short url", max_length=SLUG_LIMIT,
        example= "vercel"
    )
    makeQrcode:  bool | None = Field(
        default=False, title="argument for whether to make qrcode of short url or not; default id False",
        example= "True"
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
    longUrl: str = Field(title="Original url for update", example="https://chetan.vercel.app.com")


class TestSchema(BaseModel):
    userID : str | None  = Field(title="User ID /  USERNAME of telegram user", example=USER_ID)
    longUrl: str | None  = Field(title="Long url which is to be shorten", example="https://chetan.vercel.app.com")
    slugCode: str | None = Field(
        default=None, title="The code for short url", max_length=SLUG_LIMIT,
        example= "vercel"
    )
    clickCount: int | None  = Field(title="clicked count for the short url", example="any integer greater than equal to zero")
    createdAt : str | None  = Field(title="when short url is created", example="")