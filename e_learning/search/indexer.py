from models import Courses
from jsonschema import validate, SchemaError

SEARCH_DOCUMENT_SCHEMA = {
    "type" : "object",
    "properties" :  {
        "course_id" :         { "type" : "string" },
        "heading" :           { "type" : "string" },
        "description" :       { "type" : "string" }
        "amount" :            { "type" : "number" },
        "currency" :          { "type" : "string" },
        "seats_available" :   { "type" : "number" },
        "status":             { "type" : "string" }
        "category" :    { 
            "type" : "array",
              "items": {
                "type": "string"
              }
        },
        "teacher"  :    {
            "type" : "object",
            "properties" : {
                "full_name" : { "type" : "string"},
                "courses":    { "type" : "number"} 
            }
        }
    }
}


def build_searchable_document(course_id: int):



    try:
        validate(document, schema=SEARCH_DOCUMENT_SCHEMA)
    except SchemaError as e:
        e.add_note("Document not compatible with the existing schema")
        raise
    ##


def rebuild_index():
    pass
    ##

def index_course(course_id: int):
    pass
