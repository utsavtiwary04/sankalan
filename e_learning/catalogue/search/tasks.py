from catalogue.models import Course
from .search_clients import get_search_client 
from .search_indexer import generate_searchable_document
from celery import shared_task

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def rebuild_search_index():
    courses       = Course.all()
    search_client = get_search_client("ES")
    search_client.delete_index("elearning-search")

    for course in courses:
        document = generate_searchable_document(course)
        search_client.create_document("elearning-search", document)