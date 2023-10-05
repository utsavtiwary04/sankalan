from .search_clients import get_search_client, generate_searchable_document

def search_catalogue(query_params: dict):

    search_client = get_search_client("ES")
    query         = search_client.build_query_from_input(query_params)
    response      = search_client.search_document("elearning-search", query)

    return response

def get_recommended_courses():
    pass