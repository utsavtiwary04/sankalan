from .search_clients import get_search_client

def search_catalogue(query_params: dict):

	## build query from params
	query 		  = {"from":0,"size":10,"fields":["heading"],"query":{"bool":{"must":[{"match":{"heading":"baking"}}],"filter":[{"term":{"status":"accepting_registrations"}},{"range":{"amount":{"lte":"10999"}}}]}},"sort":{"amount":"asc"}}

	## query ES & return
	search_client = get_search_client("ES")
	query 		  = search_client.build_query_from_input(query_params)
	response 	  = search_client.search_document("elearning-search", query)

	return response

def bestseller_courses():
	pass

def recommended_for_user():
	pass

def rebuild_index():
	pass