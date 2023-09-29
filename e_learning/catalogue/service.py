from .models import Course
from .search_clients import get_search_client
from .search_indexer import generate_searchable_document
from celery import shared_task

def search_catalogue(query_params: dict):

    search_client = get_search_client("ES")
    query         = search_client.build_query_from_input(query_params)
    response      = search_client.search_document("elearning-search", query)

    return response

def get_bestseller_courses():
    # search_client = get_search_client("ES")
    pass

def get_recommended_courses():
    pass

def get_registrations(course_id: int):
    ## TODO : Finish this method referring to CourseRegistrations table
    return 12

def get_teacher(course_id: int):
    ## TODO : FInish this method referring to Users/auth

    return {
        "full_name" : "Amisha Jain",
        "gender"    : "female",
        "age"       : 34
    }

def get_courses_of_teacher(teacher_id: int):
    ## TODO : Finish this method referring to Users/auth
    # return Course.query.filter(teacher_id=teacher_id).all()

    return [Course.objects.first()]

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def rebuild_search_index():
    courses       = Course.objects.all()
    search_client = get_search_client("ES")
    search_client.delete_index("elearning-search")

    for course in courses:
        document = generate_searchable_document(course)
        search_client.create_document("elearning-search", document)
