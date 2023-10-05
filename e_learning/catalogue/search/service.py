from .search_clients  import get_search_client
from .search_indexer  import generate_searchable_document
from catalogue.models import Course

def search_catalogue(query_params: dict):

    search_client = get_search_client("ES")
    query         = search_client.build_query_from_input(query_params)
    response      = search_client.search_document("elearning-search", query)

    return response

def get_recommended_courses():
    pass


def index_course(course_id):
	course   = Course.active_course(course_id)
	document = generate_searchable_document(course)