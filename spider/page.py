from library.soup import Soup

class Page(object):
	def __init__(self, html):
		self.soup = Soup(html)
		
	def get_data(self, selector = {}):
		return self.soup.select(selector)
		
	def get_urls(self, selector = {}):
		return self.soup.find_urls(selector)