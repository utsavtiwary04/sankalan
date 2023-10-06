from .models import Course
from __common__ import service_hub as Hub
from .tasks import post_registration_tasks


def get_registrations(course_id: int):
    ## TODO : Finish this method referring to CourseRegistrations table
    return 12

def get_teacher(course_id: int, json=False):
    course  = Course.active_course(course_id)
    teacher = Hub.get_user(course.teacher_id)

    return teacher.to_json() if json else teacher

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

def pre_registration_checks(student, course):

    if not course.is_accepting_registrations():
        raise Exception(f"Course is not accepting registrations or is sold out")

    # if not Hub.is_payment_successful(student.id, course_id):
    #     raise Exception(f"Payment not completed by {student.name}({student.id}) for {course.name}({student.id})")

    if CourseRegistration.exists(course_id, student_id):
        raise Exception(f"{student.name}({student.id}) is already registered for {course_name}({course.id})")
