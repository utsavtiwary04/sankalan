from .models import Course, CourseRegistration
from .search import get_search_client, generate_searchable_document
from __common__ import service_hub as Hub
from celery import shared_task


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def rebuild_search_index():
    courses       = Course.all()
    search_client = get_search_client("ES")
    search_client.delete_index("elearning-search")

    for course in courses:
        document = generate_searchable_document(course)
        search_client.create_document("elearning-search", document)


@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def post_registration_tasks(student, course):
    all_course_registrations = CourseRegistration.registrations_of_course(course.id)

    if len(all_course_registrations) >= course.max_seats:
    	pass
        #course.update_status(Course.PAUSED_REGISTRATIONS)
        # AuditLog

    # reindex_course(course)