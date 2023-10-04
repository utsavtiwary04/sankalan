from .models import Course
from .search import get_search_client, generate_searchable_document
from __common__ import service_hub as Hub
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
    course = Course.active_course(course_id)
    return Hub.get_user(course.teacher_id).to_json()

def register_student(student_id, course_id):
    course = Course.active_course(course_id)
    if not course:
        raise Exception(f"Course does not exist :: {course_id}")
    
    student = Hub.get_user(student_id)
    if not student:
        raise Exception(f"Student does not exist :: {student_id}")

    pre_registration_checks(student, course)

    CourseRegistration = CourseRegistration(student=student, course=course)
    CourseRegistration.save()

    post_registration_tasks.delay()
    

def deregister_student(student_id, course_id):
    pass

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def rebuild_search_index():
    courses       = Course.all()
    search_client = get_search_client("ES")
    search_client.delete_index("elearning-search")

    for course in courses:
        document = generate_searchable_document(course)
        search_client.create_document("elearning-search", document)



def pre_registration_checks(student, course):

    if not course.is_accepting_registrations():
        raise Exception(f"Course is not accepting registrations or is sold out")

    if not Hub.is_payment_successful(student.id, course_id):
        raise Exception(f"Payment not completed by {student.name}({student.id}) for {course.name}({student.id})")

    if CourseRegistration.exists(course_id, student_id):
        raise Exception(f"{student.name}({student.id}) is already registered for {course_name}({course.id})")

@shared_task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def post_registration_tasks(student, course):
    all_course_registrations = CourseRegistration.registrations_of_course()

    if len(all_course_registrations) >= course.max_seats:
        course.update_status(Course.PAUSED_REGISTRATIONS)
        # AuditLog

    # reindex_course(course)

