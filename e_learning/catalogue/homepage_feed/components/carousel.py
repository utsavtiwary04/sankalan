from .base_component import BaseComponent


class Carousel(BaseComponent):

	def __init__(self,):
		self.items = []

	def validate(self):

		if len(self.items) > 0:
			for carousel_item in self.items:
				pass
