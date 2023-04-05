from fastapi import FastAPI
from instaloader import Instaloader, Profile
from pydantic import BaseModel

app = FastAPI()


class Msg(BaseModel):
    msg: str


@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}


@app.get("/path")
async def demo_get():
    return {
        "message": "This is /path endpoint, use a post request to transform the text to uppercase"
    }


@app.post("/path")
async def demo_post(inp: Msg):
    return {"message": inp.msg.upper()}


@app.get("/path/{path_id}")
async def demo_get_path_id(path_id: int):
    return {
        "message": f"This is /path/{path_id} endpoint, use post request to retrieve result"
    }


@app.get("/bot/get-insta-profile/{profile_id}")
async def get_profile_url(profile_id: str):
    response = {
        "url": Profile.from_username(
            Instaloader(
                user_agent="User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 105.0.0.11.118 (iPhone11,8; iOS 12_3_1; en_US; en-US; scale=2.00; 828x1792; 165586599)"
            ).context,
            profile_id,
        ).profile_pic_url
    }
    return response
