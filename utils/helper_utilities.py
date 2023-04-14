import json
import qrcode
from io import BytesIO
import base64
from qrcode.image.pure import PyPNGImage


def format_search_query(param1 : list, param2: list)->dict:
    """Format search query for mongoDB."""
    return dict(zip(param1, param2))


def parse_data_to_json(data: dict)-> dict:
    """
    Function to convert document fields to 
    string equivalent fields  for json serializable.
    """
    return json.loads(json.dumps(data, default=str))
 

# def parse_json(data):
#     """
#     Function to convert data fields into json serializable.
#     return  _id as string equivalent like "$oid".
#     use bson==0.5.10
#     """
#     from bson import json_util
#     return json.loads(json_util.dumps(data))
    

def generate_qr_code(url: str) -> str:
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        # print(img)
        png_img = qr.make(url, image_factory=PyPNGImage)
        print(png_img)
        # buffer = BytesIO()
        # img.save(buffer, format="PNG")
        # qr_code_image = base64.b64encode(buffer.getvalue()).decode("ascii")
        # return qr_code_image
        
        # unicode_qr_img = img.to_string(encoding='unicode')
        return png_img
