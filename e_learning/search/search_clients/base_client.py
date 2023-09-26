from abc import ABC

class BaseSearchClient(ABC):

	@abstractmethod
    def create_index(self, name):
    	pass

    @abstractmethod
	def delete_index(self, name):
		pass

	@abstractmethod
	def search_document(self, query):
		pass

	@abstractmethod
	def delete_document(self, index, doc_id):
		pass

	@abstractmethod
	def update_document(self, index, doc_id, payload):
		pass