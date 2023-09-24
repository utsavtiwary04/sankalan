from datetime import datetime
from elasticsearch import Elasticsearch


class ESClient:

	es = Elasticsearch()