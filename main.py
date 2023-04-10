import qrcode
import base64
import os
import shortuuid 
# FastAPI
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from schemas.urlShortener import Url, UrlShorten,UrlShortenUpdate, UrlSchema
from db.db_operations import  UrlShortenerDB

# instagram
from instaloader import Instaloader, Profile

# # ******************----------- End Of Imports -----------****************** 


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
url_shortner_db = UrlShortenerDB("mongodb-uri", "db-name", "collection-name")

# Templates
templates = Jinja2Templates(directory = "templates")

BASE_URL = ""
USER_ID = "chetan_jarande"

# # FastApi End points

@app.get('/', response_class = HTMLResponse)
async def index(request : Request):
    return templates.TemplateResponse("index.html", {"request" : request})

@app.post('/api/shorten', response_model = dict) 
async def create_short_url(url : UrlSchema):
    response = {}
    # convert pydantic schema object to python dict
    url = dict(url)
    slug = url.get("customCode", shortuuid.ShortUUID().random(length = 8))
    shortUrl = os.path.join(BASE_URL, slug)
    # check is url exist in DB , IF so raise an exception
    db_url_data = url_shortner_db.get_url(user_id=USER_ID, url_id=slug)
    if db_url_data:
        raise HTTPException(status_code = 400, detail = "Short code is invalid, It has been used.")
    try:
        url_data = {
            "_id": USER_ID + "-" + slug,
            "userID": USER_ID,
            "longUrl": url.get("longUrl"),
            "slug": slug,
            "shortUrl": shortUrl,
        }
        inserted = url_shortner_db.create_url(data=url_data)
        response["message"] = f"url={url['longUrl']} inserted {inserted}"
        return JSONResponse(response, 200)
    except Exception as err:
        print(err)
        response['error'] = f"An unknown error occurred. Error: {err}"
        return JSONResponse(response, 500)
    
@aap.get("/api/mongodb")
async def check_mongodb_status():
    """Hi."""
    response = {}
    try:
        url_shortner_db = UrlShortenerDB("mongodb-uri", "TelegramBots", "UrlShortner")
        response['message'] = url_shortner_db.get_url(user_id="chetan_jarande", url_id="test")
        return JSONResponse(response, 200)
    except Exception as err:
        response['error'] = f"Error: {err}"
        return JSONResponse(response, 500)





# insta profile picture url
@app.get("/bot/get-insta-profile/{profile_id}")
async def get_insta_profile_url(profile_id: str):
    response = {
        "url": Profile.from_username(Instaloader().context, profile_id).profile_pic_url
    }
    return response

