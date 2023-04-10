# import qrcode
import base64
import os
import traceback
import shortuuid

# FastAPI
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from common.config import COLLECTION_NAME, DB_NAME, MONGO_DB_URL
from db.db_operations import UrlShortenerDB
from schemas.urlShortener import UrlSchema

# instagram
from instaloader import Instaloader, Profile

# # other 
from common.constants import USER_ID

# # ******************----------- End Of Imports -----------******************


app = FastAPI()

# Templates
templates = Jinja2Templates(directory="templates")

# Create an instance of the database wrapper class
url_shortner_db = UrlShortenerDB(
    db_url=MONGO_DB_URL, db_name=DB_NAME, collection_name=COLLECTION_NAME
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # FastApi End points
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/shorten", response_model=dict)
async def create_short_url(url: UrlSchema):
    response = {}
    try:
        # convert pydantic schema object to python dict
        url = dict(url)
        slug = url.get("customSlugCode", shortuuid.ShortUUID().random(length=8))

        # check is url exist in DB , IF so raise an exception
        db_url_data = url_shortner_db.get_url_data_by_slug(slug=slug)
        if db_url_data:
            raise HTTPException(status_code=400, detail="Slug code is invalid, It has been used.")
        url_data = {
            "userID": USER_ID,
            "longUrl": url.get("longUrl"),
            "slug": slug,
        }
        inserted = url_shortner_db.create_url(data=url_data)
        response["message"] = f"url={url['longUrl']} inserted {inserted}"
        response['data'] = url_data
        return JSONResponse(response, 200)
    except Exception as err:
        response["error"] = f"An Error occurred. Error: {err} \nTraceback : {traceback.format_exc()}"
        return JSONResponse(response, 500)


@app.get("/api/get/slugs/{user_id}")
async def get_slugs_for_user(user_id: str) -> list:
    """Get slugs for a particular user."""
    response = {}
    try:
        urls_data = url_shortner_db.get_urls_data_by_user_id(user_id="chetan_jarande")
        if len(urls_data) > 0:
            response["data"] = urls_data
        else:
            response['message'] = f"no data found for a user {user_id}"
        return JSONResponse(response, 200)
    except Exception as err:
        response["error"] = f"Error: {err}. \nTraceback : {traceback.format_exc()}"
        return JSONResponse(response, 500)

@app.get("/api/test")
async def test():
    response = {}
    try:
        response = {
            "get_urls_data_by_user_id": url_shortner_db.get_urls_data_by_user_id(user_id=USER_ID),
            "get_data_by_user_and_slug": url_shortner_db.get_data_by_user_and_slug(user_id=USER_ID, slug="Gamil"),
            "get_url_data_by_slug": url_shortner_db.get_url_data_by_slug(slug="test")
        }
        return JSONResponse(response, 200)
    except Exception as err:
        response['error'] = f"error : {err} \nTraceback : {traceback.format_exc()}"
        return JSONResponse(response, 500)

@app.get("/{slug}")
async def redirect_slug(slug: str):
    """Redirect of slug url using Long url."""
    response = {}
    try:
        slug_data = url_shortner_db.get_url_data_by_slug(slug=slug)
        if not slug_data:
            raise HTTPException(status_code= 404, detail = "URL not found !")
        response = RedirectResponse(url = slug_data["longUrl"])
        return JSONResponse(response, 200)
    except Exception as err:
        response['error'] = f"Error {err} \nTraceback : {traceback.format_exc()}"
        return JSONResponse(response, 500)


# insta profile picture url
@app.get("/bot/get-insta-profile/{profile_id}")
async def get_insta_profile_url(profile_id: str):
    response = {
        "url": Profile.from_username(Instaloader().context, profile_id).profile_pic_url
    }
    return response
