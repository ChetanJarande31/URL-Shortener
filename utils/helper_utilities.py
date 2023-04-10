def format_search_query(param1 : list, param2: list)->dict:
    """Format search query for mongoDB."""
    return dict(zip(param1, param2))
