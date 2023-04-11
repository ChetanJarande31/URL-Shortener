# import qrcode
# from io import BytesIO
# from bson import ObjectId
import base64
from datetime import datetime

from pymongo import MongoClient

from utils.helper_utilities import format_search_query, parse_data_to_json


class UrlShortenerDB:
    def __init__(self, db_url: str, db_name: str, collection_name: str):
        self.db_client = MongoClient(db_url)
        self.db = self.db_client[db_name]
        self.collection = self.db[collection_name]

    def create_url(self, data: dict) -> str:
        result = self.collection.insert_one(
            {**data, "clickCount": 0, "createdAt": datetime.now()}
        )
        return result

    def get_url_data_by_slug(self, slug: str) -> dict:
        """Get url data by slug."""
        return parse_data_to_json(self.collection.find_one({"slug": slug}))

    def get_data_by_user_and_slug(self, user_id: str, slug: str) -> dict:
        """Get Url by user ID and Slug."""
        return parse_data_to_json(
            self.collection.find_one(
                format_search_query(["userID", "slug"], [user_id, slug])
            )
        )

    def get_urls_data_by_user_id(self, user_id: str) -> list:
        """Find Urls by user ID."""
        return list(
            map(
                parse_data_to_json,
                self.collection.find(format_search_query(["userID"], [user_id])),
            )
        )

    def update_url(self, user_id: str, slug: str, long_url: str) -> bool:
        is_present = self.get_data_by_user_and_slug(user_id, slug=slug)
        if is_present:
            result = self.collection.update_one(
                {"userID": user_id, "slug": slug}, {"$set": {"longUrl": long_url}}
            )
            return result.modified_count > 0
        else:
            return False

    def delete_url(self, user_id: str, slug: str) -> bool:
        result = self.collection.delete_one({"userID": user_id, "slug": slug})
        return result.deleted_count > 0

    def increment_click_count(self, user_id: str, slug: str) -> None:
        self.collection.update_one(
            {"userID": user_id, "slug": slug}, {"$inc": {"clickCount": 1}}
        )

    # # def generate_qr_code(self, url: str) -> str:
    # #     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    # #     qr.add_data(url)
    # #     qr.make(fit=True)
    # #     img = qr.make_image(fill_color="black", back_color="white")
    # #     buffer = BytesIO()
    # #     img.save(buffer, format="PNG")
    # #     qr_code_image = base64.b64encode(buffer.getvalue()).decode("ascii")
    # #     return qr_code_image
