import json
# from bson import json_util


def format_search_query(param1 : list, param2: list)->dict:
    """Format search query for mongoDB."""
    return dict(zip(param1, param2))

def parse_data_to_json(data: dict)-> dict:
    """
    Function to convert _id or object filed to 
    string equivalent fields  for json serializable.
    """
    return json.loads(json.dumps(data, default=str))
 


# def parse_json(data):
#     """
#     Function to convert data fields into json serializable.
#     return  _id as string equivalent like "$oid".
#     use bson==0.5.10
#     """
#     return json.loads(json_util.dumps(data))
    

