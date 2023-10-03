import csv
import requests

class CSV():

	def __init__(self, file_url: str, delimiter=",", headers=[]):
		self.file_path = file_url

		try:
			response 	  = requests.get(file_url, timeout=10)
			response_data = list(line.decode('utf-8') for line in response.iter_lines())
			csv_reader    = csv.reader(response_data, delimiter=',')
		
			self.raw_data        = list(csv_reader)
			self.raw_headers     = headers or self.raw_data.pop(0)
			self.structured_data = [dict(zip(self.raw_headers, item)) for item in self.raw_data]

		except Exception as e:
			# log
			raise Exception(f"Error in importing CSV file :: {e}")

	def data(self):
		return self.structured_data

	def headers(self):
		return self.raw_headers
