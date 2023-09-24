import json
from copy import deepcopy
from datetime import datetime

import pytz
import requests
from requests.auth import HTTPBasicAuth
from structlog import get_logger

from celery_manager import celery_app
from config import Config

logger = get_logger()
conf = Config()


ES_URL      = conf.DATABASE["ES_URL"]
ES_URL_NEW  = conf.DATABASE["ES_URL_NEW"]
ES_USERNAME = conf.DATABASE["ES_USERNAME"]
ES_PASSWORD = conf.DATABASE["ES_PASSWORD"]
AUTH_TOKEN  = conf.DATABASE.get("ES_AUTH_TOKEN")
ENGINE      = 'courses'


def add_id_to_doc(hit):
    try:
        allowed_script_fields = ['is_registered']
        enhanced_doc = deepcopy(hit['_source'])
        enhanced_doc['id'] = hit['_id']
        for field, val in hit.get('fields', {}).items():
            if field in allowed_script_fields:
                enhanced_doc[field] = val[0] if isinstance(val, list) and len(val) == 1 else val
        return enhanced_doc
    except Exception as e:
        logger.error(f"Failed to add id to doc.",
                     error=str(e))
        return None


def minimal_doc(hit):
    try:
        enhanced_doc = deepcopy(hit['_source'])
        if "registered_students" in enhanced_doc:
            enhanced_doc.pop("registered_students")
        for demo in enhanced_doc.get("demos", []):
            if "registered_students" in demo:
                demo.pop("registered_students")
        return enhanced_doc
    except Exception as e:
        logger.error(f"Failed to add id to doc.",
                     error=str(e))
        return None

"""
############################################

NEW ELASTIC REQUESTS https://bitclass-staging.es.ap-south-1.aws.elastic-cloud.com:9243" BASIC AUTHENTICATION

############################################
"""


def create_index(index, index_config=None):
    if index_config is None:
        index_config = {}

    try:
        response = requests.put(
            f"{ES_URL_NEW}/{index}",
            data=json.dumps(index_config),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD))

        print(response.text)
        if response.status_code > 201:
            logger.error(f"Failed to create index",
                         error=response.status_code,
                         index=index)
            return False

        return True

    except Exception as e:
        logger.error(f"Failed to create index", error=str(e), index=str(index))
        return False


def delete_index(index):
    try:
        response = requests.delete(
            f"{ES_URL_NEW}/{index}",
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to delete index",
                         error=response.status_code,
                         index=index)
            return False

        return True

    except Exception as e:
        logger.error(f"Failed to delete index",
                     error=str(e),
                     index=str(index))
        return False


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
def create_or_update_document(index, doc_id=None, doc=None):
    if doc is None:
        doc = {}
    try:
        doc['updated_at'] = pytz.utc.localize(datetime.utcnow()).isoformat()
        response = requests.post(
            f"{ES_URL_NEW}/{index}/_update/{doc_id}",
            data=json.dumps({"doc": doc, "doc_as_upsert": True}),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD))

        if response.status_code > 201:
            logger.error(f"Failed to update document {doc['doc_id']}",
                         error=str(response.json()),
                         index=index)
            return None

        return response.json()["_id"]

    except Exception as e:
        logger.error(f"Failed to update",
                     index=str(index),
                     doc_id=str(doc['doc_id']),
                     error=str(e))
        raise Exception(f"Failed to update {str(index)} {str(doc['doc_id'])}")


def get_document(index, doc_id):
    try:
        response = requests.get(
            f"{ES_URL_NEW}/{index}/_doc/{doc_id}",
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD))

        if response.status_code > 201:
            logger.warn(f"Failed to get document {doc_id}",
                         error=response.status_code,
                         index=index)
            return {}

        doc = response.json()
        if not doc["found"]:
            return {}

        # TODO : Deleted entities to be handled
        # if doc["_source"]["deleted_at"]:
        #     raise Exception(f"No such {self.index} {doc_id} exists")

        return add_id_to_doc(doc)

    except Exception as e:
        logger.error(f"Failed to get doc.",
                     index=str(index),
                     doc_id=str(doc_id),
                     error=str(e))
        return {}
        # raise Exception(f"Failed to get {index} {doc_id}")


def search_document(index, query):
    try:
        response = requests.post(
            f"{ES_URL_NEW}/{index}/_search",
            data=json.dumps(query),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to search document {query}",
                         error=response.status_code,
                         error_text=response.text,
                         index=index)
            return [], 0, {}

        aggregations = {}
        if "aggregations" in response.json():
            aggregations = response.json()["aggregations"]

        return [add_id_to_doc(hit) for hit in response.json()['hits']['hits']], response.json()['hits']['total'][
            'value'], aggregations

    except Exception as e:
        logger.error(f"Failed to search",
                     index=str(index),
                     query=str(query),
                     error=str(e))
        raise Exception(f"Failed to search {str(index)} {str(query)} {str(e)}")


def delete_document_by_doc_id(index, doc_id):
    try:
        response = requests.delete(
            f"{ES_URL_NEW}/{index}/_doc/{doc_id}",
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to delete document",
                         error=response.status_code,
                         index=index)
            return False

        return True

    except Exception as e:
        logger.error(f"Failed to update",
                     index=str(index),
                     doc_id=doc_id,
                     error=str(e))
        return False


def delete_document(index, query):
    try:
        query = {
            "query":
                {
                    "match": query
                }
        }
        response = requests.post(
            f"{ES_URL_NEW}/{index}/_delete_by_query",
            data=json.dumps(query),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to delete document",
                         error=response.status_code,
                         index=index)
            return False

        return True

    except Exception as e:
        logger.error(f"Failed to update",
                     index=str(index),
                     doc_id=str(query),
                     error=str(e))
        return False


def update_document(index, doc_id, doc):
    try:
        doc['updated_at'] = pytz.utc.localize(datetime.utcnow()).isoformat()
        response = requests.post(
            f"{ES_URL_NEW}/{index}/_update/{doc_id}",
            data=json.dumps({"doc": doc, "doc_as_upsert": True}),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to update document",
                         doc_id=str(doc_id),
                         error=response.status_code,
                         index=index)
            return None

        return response.json()["_id"]

    except Exception as e:
        logger.error(f"Failed to update",
                     index=str(index),
                     doc_id=str(doc_id),
                     doc=str(doc),
                     error=str(e))
        raise Exception(f"Failed to update {str(index)} {str(doc_id)}")


def create_new_document(index, doc):
    try:
        doc['created_at'] = pytz.utc.localize(datetime.utcnow()).isoformat()
        doc['deleted_at'] = None

        response = requests.post(
            f"{ES_URL_NEW}/{index}/_doc/{doc['doc_id']}",
            data=json.dumps(doc),
            headers={"Content-Type": "application/json"},
            auth=HTTPBasicAuth(ES_USERNAME, ES_PASSWORD)
        )

        if response.status_code > 201:
            logger.error(f"Failed to create document",
                         doc_id=doc['doc_id'],
                         error=response.status_code,
                         error_message=response.text,
                         index=index)
            return None

        return response.json()["_id"]

    except Exception as e:
        logger.error(f"Failed to to create new index",
                     index=str(index),
                     error=str(e),
                     doc=str(doc)
                     )
        raise Exception(f"Failed to create new {str(index)}")
