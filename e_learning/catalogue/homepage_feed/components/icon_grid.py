from .base_component import BaseComponent
from .constants import *

class IconGrid(BaseComponent):

	def __init__(self,):
		self.items   = []
		self.length  = 2
		self.breadth = 2

	def validate(self):

		if len(self.items) > 0:
			for carousel_item in self.items:
				pass
