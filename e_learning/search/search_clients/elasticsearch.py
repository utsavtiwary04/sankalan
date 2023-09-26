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


ES_URL      = "https://localhost:9200"
ES_USERNAME = "elastic"
ES_PASSWORD = "pzYymOMRt=-pdvfwbj*d"


class ESClient(BaseSearchClient):

    def __init__(self, URL=ES_URL, username=ES_USERNAME, password=ES_PASSWORD):
        self.URL = URL
        self.username = username
        self.password = password

    def format_response(self, hit):
        try:
            enhanced_doc = deepcopy(hit['_source'])
            enhanced_doc['id'] = hit['_id']
            return enhanced_doc

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

    def delete_index(self, index):
        try:
            response = requests.delete(
                f"{self.URL}/{index}",
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
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


    # @celery_app.task(autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 2})
    # def create_or_update_document(index, doc_id=None, doc=None):
    #     if doc is None:
    #         doc = {}
    #     try:
    #         doc['updated_at'] = pytz.utc.localize(datetime.utcnow()).isoformat()
    #         response = requests.post(
    #             f"{self.URL}/{index}/_update/{doc_id}",
    #             data=json.dumps({"doc": doc, "doc_as_upsert": True}),
    #             headers={"Content-Type": "application/json"},
    #             auth=HTTPBasicAuth(self.username, self.password))

    #         if response.status_code > 201:
    #             logger.error(f"Failed to update document {doc['doc_id']}",
    #                          error=str(response.json()),
    #                          index=index)
    #             return None

    #         return response.json()["_id"]

    #     except Exception as e:
    #         logger.error(f"Failed to update",
    #                      index=str(index),
    #                      doc_id=str(doc['doc_id']),
    #                      error=str(e))
    #         raise Exception(f"Failed to update {str(index)} {str(doc['doc_id'])}")

    def create_document(self, index, doc):
        try:
            response = requests.post(
                f"{self.URL}/{index}/_doc/{doc['doc_id']}",
                data=json.dumps(doc),
                headers={"Content-Type": "application/json"},
                auth=HTTPBasicAuth(self.username, self.password)
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
                return [], 0, {}

            return [self.format_response(hit) for hit in response.json()['hits']['hits']], response.json()['hits']['total'][
                'value']

        except Exception as e:
            logger.error(f"Failed to search",
                         index=str(index),
                         query=str(query),
                         error=str(e))
            raise Exception(f"Failed to search {str(index)} {str(query)} {str(e)}")

    def update_document(self, index, doc_id, doc):
        try:
            # doc['updated_at'] = pytz.utc.localize(datetime.utcnow()).isoformat() TODO
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
                return False

            return True

        except Exception as e:
            logger.error(f"Failed to update",
                         index=str(index),
                         doc_id=doc_id,
                         error=str(e))
            return False



