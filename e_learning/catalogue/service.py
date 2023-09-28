from .search_clients import get_search_client

def search_catalogue(query_params: dict):

	search_client = get_search_client("ES")
	query 		  = search_client.build_query_from_input(query_params)
	response 	  = search_client.search_document("elearning-search", query)

	return response

def bestseller_courses():
	# search_client = get_search_client("ES")
	pass

def recommended_for_user():
	pass

def rebuild_index():
	pass