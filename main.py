from fastapi import FastAPI, requests, HTTPException
from instaloader import Instaloader, Profile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import qrcode
import base64

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create an instance of the database wrapper class
db = UrlShortenerDB("mongodb-uri", "db-name", "collection-name")



@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}

# insta profile picture url 
@app.get("/bot/get-insta-profile/{profile_id}")
async def get_insta_profile_url(profile_id: str):
    response = {
        "url": Profile.from_username(Instaloader().context, profile_id).profile_pic_url
    }
    return response

