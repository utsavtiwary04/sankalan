from .search_clients  import get_search_client
from .search_indexer  import generate_searchable_document
from catalogue.models import Course
from catalogue.pricing.service import get_prices

def search_catalogue(query_params: dict, user_id=None):

    search_client = get_search_client("ES")
    query         = search_client.build_query_from_input(query_params)
    response      = search_client.search_document("elearning-search", query)

    ## Get pricing
    course_ids    = [course["id"] for course in response]
    prices        = get_prices(course_ids, user_id)

    ## Merge the response
    return [{ **course, **price } for course, price in zip(response, prices)]

def get_recommended_courses():
    pass


def index_course(course_id):
    course        = Course.active_course(course_id)
    document      = generate_searchable_document(course)
    search_client = get_search_client("ES")
