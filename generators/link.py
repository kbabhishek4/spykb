class Link(object):
	def __init__(self, link_data):
		self.link_data = link_data
		
	def generate(self):
		for link in self.link_data:
			yield link