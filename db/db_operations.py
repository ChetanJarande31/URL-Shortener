import qrcode
from io import BytesIO
import base64
from pymongo import MongoClient
from bson import ObjectId


class UrlShortenerDB:
    def __init__(self, db_uri: str, db_name: str, collection_name: str):
        self.client = MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def create_url(self, user_id: str, url: str) -> str:
        result = self.collection.insert_one({"user_id": user_id, "url": url, "click_count": 0})
        return str(result.inserted_id)

    def get_url(self, user_id: str, url_id: str) -> dict:
        url_object = self.collection.find_one({"user_id": user_id, "_id": ObjectId(url_id)})
        return url_object

    def get_all_urls(self, user_id: str) -> list:
        urls = []
        for url_object in self.collection.find({"user_id": user_id}):
            urls.append({"id": str(url_object["_id"]), "url": url_object["url"], "click_count": url_object["click_count"]})
        return urls

    def update_url(self, user_id: str, url_id: str, url: str) -> bool:
        result = self.collection.update_one({"user_id": user_id, "_id": ObjectId(url_id)}, {"$set": {"url": url}})
        return result.modified_count > 0

    def delete_url(self, user_id: str, url_id: str) -> bool:
        result = self.collection.delete_one({"user_id": user_id, "_id": ObjectId(url_id)})
        return result.deleted_count > 0

    # def generate_qr_code(self, url: str) -> str:
    #     qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    #     qr.add_data(url)
    #     qr.make(fit=True)
    #     img = qr.make_image(fill_color="black", back_color="white")
    #     buffer = BytesIO()
    #     img.save(buffer, format="PNG")
    #     qr_code_image = base64.b64encode(buffer.getvalue()).decode("ascii")
    #     return qr_code_image

    def increment_click_count(self, user_id: str, url_id: str) -> None:
        self.collection.update_one({"user_id": user_id, "_id": ObjectId(url_id)}, {"$inc": {"click_count": 1}})
