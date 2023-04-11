import json
from bson import json_util


def format_search_query(param1 : list, param2: list)->dict:
    """Format search query for mongoDB."""
    return dict(zip(param1, param2))


def parse_json(data):
    """
    Function to convert data fields into json serializable.
    return  _id as string equivalent like "$oid".
    """
    return json.loads(json_util.dumps(data))
    

