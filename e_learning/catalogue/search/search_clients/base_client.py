from abc import ABC, abstractmethod

class BaseSearchClient(ABC):

    @abstractmethod
    def create_index(self, name):
        pass

    @abstractmethod
    def delete_index(self, name):
        pass

    @abstractmethod
    def create_document(index, doc):
        pass

    @abstractmethod
    def search_document(self, index, query):
        pass

    @abstractmethod
    def update_document(self, index, doc_id, doc):
        pass

    @abstractmethod
    def delete_document(self, index, doc_id):
        pass

    @staticmethod
    def build_query_from_input(query_params):
        pass

def get_search_client(source="ES"):
    from .elasticsearch import ESClient
    # Circular import will be resolve if this selector method is put in a separate file. Low prio.

    if source == "ES":
        return ESClient()

    # [TODO]
    # if source == "MONGO":
    #     return MongoClient()
