"""@@@
Here is a sample document that we want to index, search and return. 
It is a good idea to construct an example with real data before beginning to code as 
it helps in visualizing how our index would eventually look like.

 {
    "course_id" : "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "heading" : "Summer Baking : 15 Recipes",
    "description" : "Le Cordon Bleu has a large variety of cookery courses available every summer. From classes of just a few hours to formally accredited 6/7 week courses, you should be able to find the cooking course that would suit you best. Our culinary courses are a wonderful way to learn more about the fundamental techniques in cuisine, pâtisserie or wine in entertaining and informal classes. Whether you are preparing for a professional cooking career or just wish to study over the summer for your own interest you should be able to find a summer programme for you.",
    "amount" : 5699,
    "currency" : "INR",
    "status": "accepting_registrations",
    "category" : ["baking", "recreational", "adults", "kids"],
    "seats_available" :  20,
    "teacher"  :    {
        "full_name" : "Amisha Jain",
        "courses_taken": 12
    },
    "schedule": {
        "start_date": "24 August, 2021",
        "end_date": "29 August, 2021",
        "duration": "60 mins",
        "sessions": 4,
        "session_start_timings": [1695571696, 1695571800, 1695572696, 1695573696]
    }
}
@@@"""


SEARCH_DOCUMENT_SCHEMA = {
    "type" : "object",
    "properties" :  {
        "course_id" :         { "type" : "number" },
        "heading" :           { "type" : "string" },
        "description" :       { "type" : "string" },
        "amount" :            { "type" : "number" },
        "currency" :          { "type" : "string" },
        "seats_available" :   { "type" : "number" },
        "status":             { "type" : "string" },
        "category" :          { "type" : "string" },
        "teacher"  :    {
            "type" : "object",
            "properties" : {
                "full_name" : { "type" : "string"},
                "courses":    { "type" : "number"} 
            }
        },
        "schedule": {
            "type": "object",
            "properties": {
                "start_date": { "type" : "string" },
                "end_date": { "type"   : "string" },
                "duration": { "type"   : "number" },
                "sessions": { "type"   : "number" }
            }
        }
    }
}


def generate_searchable_document(course):
    from catalogue.models import Course
    from catalogue.service import get_registrations, get_teacher
    from catalogue.search.search_clients import get_search_client
    from jsonschema import validate, SchemaError

    try:
        teacher  = get_teacher(course.id)
        document =  {
            "course_id"         : course.id,
            "heading"           : course.heading,
            "description"       : course.description,
            "amount"            : float(course.amount),
            "currency"          : course.currency,
            "status"            : course.status,
            "category"          : course.category.display_text,
            "seats_available"   : course.max_seats - get_registrations(course.id),
            "teacher": {
                "full_name"     : teacher.full_name(),
                "courses_taken" : len(Course.all_courses_of_teacher(teacher.id))
            },
            "schedule": {
                "start_date"    : course._start_date("%d-%m-%Y"),
                "end_date"      : course._end_date("%d-%m-%Y"),
                "duration"      : course.duration,
                "sessions"      : course.sessions
            }
        }
        validate(document, schema=SEARCH_DOCUMENT_SCHEMA)

        return document

    except SchemaError as e:
        e.add_note("Document not compatible with the existing schema")
        raise
