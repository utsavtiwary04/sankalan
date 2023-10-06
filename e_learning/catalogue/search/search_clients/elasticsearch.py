import json
from copy import deepcopy
from datetime import datetime


import pytz
import requests
from requests.auth import HTTPBasicAuth
from .base_client import BaseSearchClient
from structlog import get_logger

logger = get_logger()

# from celery_manager import celery_app
# from config import Confige


ES_URL      = "http://localhost:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "pzYymOMRt=-pdvfwbj*d"


class ESClient(BaseSearchClient):

    def __init__(self, URL=ES_URL, username=ES_USERNAME, password=ES_PASSWORD):
        self.URL = URL
        self.username = username
        self.password = password

    def format_response(self, hit):
        try:
            response_doc = deepcopy(hit['_source'])
            response_doc['id'] = hit['_id']
            return response_doc

        except Exception as e:
            logger.error(f"Failed to add id to doc.",
                         error=str(e))
            return None

    def create_index(self, index, index_config=None):
        if index_config is None:
            index_config = {}

        try:
            response = requests.put(
                f"{self.URL}/{index}",
                data=json.dumps(index_config),
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password))

            if response.status_code > 201:
                logger.error(f"Failed to create index",
                             error=response.status_code,
                             index=index)
                raise Exception(f"Failed to create index :: {str(index)}")

        except Exception as e:
            logger.error(f"Failed to create index", error=str(e), index=str(index))
            raise Exception(f"Failed to create index :: {str(index)}")

    def delete_index(self, index):
        try:
            response = requests.delete(
                f"{self.URL}/{index}/?ignore_unavailable=true",
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
            )

            if response.status_code > 201:
                logger.error(f"Failed to delete index",
                             error=response.status_code,
                             index=index)
                raise Exception(f"Failed to delete index :: {str(index)}")

        except Exception as e:
            logger.error(f"Failed to delete index",
                         error=str(e),
                         index=str(index))
            raise Exception(f"Failed to delete index :: {str(index)}")

    def create_document(self, index, doc):
        try:
            response = requests.post(
                f"{self.URL}/{index}/_doc/",
                data=json.dumps(doc),
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
            )

            if response.status_code > 201:
                logger.error(f"Failed to create document",
                             doc_id=doc.get("_id"),
                             error=response.status_code,
                             error_message=response.text,
                             index=index)
                raise Exception(f"Failed to create new document in {str(index)}")

            return response.json()["_id"]

        except Exception as e:
            logger.error(f"Failed to to create new document",
                         index=str(index),
                         error=str(e),
                         doc=str(doc)
                         )
            raise Exception(f"Failed to create new document in {str(index)}")

    def search_document(self, index, query):
        try:
            response = requests.post(
                f"{self.URL}/{index}/_search",
                data=json.dumps(query),
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password),
                verify=False
            )

            if response.status_code > 201:
                logger.error(f"Failed to search document {query}",
                             error=response.status_code,
                             error_text=response.text,
                             index=index)
                raise Exception(f"Failed to search in index :: {str(index)} - {response.text}")

            return [self.format_response(hit) for hit in response.json()['hits']['hits']]

        except Exception as e:
            logger.error(f"Failed to search",
                         index=str(index),
                         query=str(query),
                         error=str(e))
            raise Exception(f"Failed to search in index :: {str(index)} - {str(e)}")

    def update_document(self, index, doc_id, doc):
        try:
            response = requests.post(
                f"{self.URL}/{index}/_update/{doc_id}",
                data=json.dumps({"doc": doc, "doc_as_upsert": True}),
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
            )

            if response.status_code > 201:
                logger.error(f"Failed to update document",
                             doc_id=str(doc_id),
                             error=response.status_code,
                             error_message=response.text,
                             index=index)
                raise Exception(f"Failed to update document :: {str(index)} - {error_message}")

            return response.json()["_id"]

        except Exception as e:
            logger.error(f"Failed to update",
                         index=str(index),
                         doc_id=str(doc_id),
                         doc=str(doc),
                         error=str(e))
            raise Exception(f"Failed to update document :: {str(index)} - {error}")

    def delete_document(self, index, doc_id):
        try:
            response = requests.delete(
                f"{self.URL}/{index}/_doc/{doc_id}",
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
            )

            if response.status_code > 201:
                logger.error(f"Failed to delete document",
                             error=response.status_code,
                             index=index)
                raise Exception(f"Failed to delete document :: {str(index)} - {error_message}")

            return True

        except Exception as e:
            logger.error(f"Failed to update",
                         index=str(index),
                         doc_id=doc_id,
                         error=str(e))
            raise Exception(f"Failed to delete document :: {str(index)} - {error}")

    def build_query_from_input(self, query_params):

        def is_key_present(obj, key):
            return (key in obj) and (obj[key] is not None) and (obj[key]) 
        ## This can be a design pattern in itself : Adapter or builder
        es_query = {}

        ## Extract search query
        if is_key_present(query_params, "keyword"):
            es_query = {
                "query" : {
                    "bool" : {
                        "must" : [
                            {
                                "match": {
                                    "heading": query_params["keyword"]
                                }
                            }
                        ]
                    }
                }
            }


        filters = []
        ## Extract filters
        #### Price filter
        if is_key_present(query_params, "amount__lte"):
            filters.append({ "range": { "amount" : { "lte" : query_params["amount__lte"] }}})

        if is_key_present(query_params, "amount__gte"):
            filters.append({ "range": { "amount" : { "gte" : query_params["amount__gte"] }}})

        #### Date filter
        if is_key_present(query_params, "startdate__gte"):
            filters.append({ "range": { "schedule.start_date" : { "gte" : query_params["startdate__gte"] }}})

        if is_key_present(query_params, "enddate_lte"):
            filters.append({ "range": { "schedule.end_date" : { "gte" : query_params["enddate_lte"] }}})

        #### Session count filter
        if is_key_present(query_params, "sessions__lte"):
            filters.append({ "range": { "schedule.sessions" : { "gte" : query_params["sessions__lte"] }}})

        if is_key_present(query_params, "sessions__gte"):
            filters.append({ "range": { "schedule.sessions" : { "gte" : query_params["sessions__gte"] }}})

        if len(filters) > 0:
            es_query["query"] = {
                "bool" : {
                    "filter" : filters
                }
            }


        ## Extract sort param
        if is_key_present(query_params, "sort_by"):
            es_query["sort"] = {
                query["sort_by"] : query["order"] if is_key_present(query_params, "order") else "desc"
            }

        ## Extract limit & offset
        if is_key_present(query_params, "limit"):
            es_query["size"] = query_params["limit"]

        if is_key_present(query_params, "offset"):
            es_query["from"] = query_params["offset"]

        return es_query

    # def reindex_course(self, index, course_id, doc):
    #     current_doc = self.search_document(index, { })
    #     return self.update_document(index, current_doc["_id"], doc)
