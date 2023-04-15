# import qrcode
import base64
import os
import json
import traceback
import shortuuid

# FastAPI
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder

# instagram
from instaloader import Instaloader, Profile
from instaloader.exceptions import ProfileNotExistsException

# # other
from common.config import COLLECTION_NAME, DB_NAME, MONGO_DB_URL
from common.constants import SLUG_LIMIT, USER_ID
from db.db_operations import UrlShortenerDB
from schemas.urlShortener import UrlSchema, UrlUpdateSchema, TestSchema
from utils.helper_utilities import generate_qr_code

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
    # print(f"{(json.dumps(dict(request),default=str, indent=4))}")
    # print(f"{request.client}")
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/shorten", response_model=dict)
async def create_short_url(url: UrlSchema):
    response = {}
    try:
        # convert pydantic schema object to python dict
        url = dict(url)
        slug = url.get("customSlugCode") if url.get('customSlugCode') else shortuuid.ShortUUID().random(length=SLUG_LIMIT)
        
        # check is url exist in DB , IF so raise an exception
        db_url_data = url_shortner_db.get_url_data_by_slug(slug=slug)
        if db_url_data:
            raise HTTPException(status_code=404, detail=f"Slug code is invalid, It has been used. found {db_url_data}")
        url_data = {
            "userID": USER_ID,
            "longUrl": url.get("longUrl"),
            "slug": slug,
        }
        # if url.get('makeQrcode'):
        #     response['qr_code'] = generate_qr_code(url=url.get("longUrl"))
        inserted = url_shortner_db.create_url(data=url_data)
        response = {
            'message': f"create short url for url={url['longUrl']}",
            'data': url_data,
            'inserted': inserted,
        }
        return JSONResponse(response, 200)
    except HTTPException as http_exception:
        response['error'] = http_exception.detail
        return JSONResponse(response, http_exception.status_code)
    except Exception as err:
        response[
            "error"
        ] = f"An Error occurred. Error: {err}"
        response['traceback'] = traceback.format_exc()
        return JSONResponse(response, 500)


@app.get("/api/get/slugs/{user_id}")
async def get_slugs_for_user(user_id: str) -> list:
    """Get slugs for a particular user."""
    response = {}
    try:
        urls_data = url_shortner_db.get_urls_data_by_user_id(user_id=user_id)
        if len(urls_data) > 0:
            response["data"] = urls_data
        else:
            response["message"] = f"no data found for a user {user_id}"
        return JSONResponse(response, 200)
    except Exception as err:
        response["error"] = f"Error: {err}."
        response['traceback'] = traceback.format_exc()
        return JSONResponse(response, 500)


@app.put("/api/update/{user_id}/slug/{slug_id}")
async def get_slug_data(user_id: str, slug_id: str, update_url: UrlUpdateSchema):
    response = {}
    long_url = update_url.longUrl
    try:
        result = url_shortner_db.update_url(user_id=user_id, slug=slug_id, long_url=long_url)
        response['message'] = (
            f'Successfully update the URL={long_url} for User: {user_id} & Slug:{slug_id}.' 
            if result 
            else f"Provided Slug={slug_id} does not exist in DB."
        )
        return JSONResponse(response, 200)
    except Exception as err:
        response['error'] = err
        response['traceback'] = traceback.format_exc()
        return JSONResponse(response, 500)


# # API redirection for Slug
@app.get("/{slug}", response_class=RedirectResponse)
async def redirect_slug(slug: str):
    """Redirect of slug url using Long url."""
    response = {}
    try:
        slug_data = url_shortner_db.get_url_data_by_slug(slug=slug)
        if not slug_data:
            raise HTTPException(status_code=404, detail="URL not found !")
        url_shortner_db.increment_click_count(user_id=slug_data['userID'], slug=slug_data['slug'])
        return slug_data.get("longUrl")
    except HTTPException as err:
        response["error"] = f'url not found for parameter: {slug}'
        return JSONResponse(response, 404)
    except Exception as err:
        response["error"] = f"{err}"
        response['traceback'] = traceback.format_exc()
        return JSONResponse(response, 500)


@app.post("/api/test/{method}")
async def test(method: str, test_schema: TestSchema, request: Request):
    response = {}
    try:
        if method == "get":
            response = {
                "get_urls_data_by_user_id": url_shortner_db.get_urls_data_by_user_id(
                    user_id=test_schema.userID
                ),
                "get_data_by_user_and_slug": url_shortner_db.get_data_by_user_and_slug(
                    user_id=test_schema.userID, slug= test_schema.slugCode or "Gamil" 
                ),
                "get_url_data_by_slug": url_shortner_db.get_url_data_by_slug(slug= test_schema.slugCode or "MyGithub"),
                'request': request.client.host,
            }
        elif method == 'deleteMany':
            data = {
                'userID': test_schema.userID or 'CHETAN_JARANDE',
                'longUrl': test_schema.longUrl or 'https://github.com/Chetan_Jarande31',
            }
            response = {
                'delete_many': url_shortner_db.delete_many_url(filter_data=data),
                'filter_data': data,
            }
        else:
            response["error"] = f'provided method={method} is invalid.'
        return JSONResponse(response, 200)
    except Exception as err:
        response["error"] = f"error : {err}."
        response['traceback'] = traceback.format_exc()
        return JSONResponse(response, 500)


# # *****************------------------------ Instagram Loader ------------------------*****************

# insta profile picture url
@app.get("/api/instagram/get-insta-profile/{profile_id}")
async def get_insta_profile_url(profile_id: str):
    response= {}
    try:
        response = {
            "instagramProfilePicUrl": Profile.from_username(Instaloader().context, profile_id).profile_pic_url
        }
    except ProfileNotExistsException as insta_profile_not_exist_exception:
        response['error'] = str(insta_profile_not_exist_exception)
    except Exception as err:
        response['error'] = err
    return response
