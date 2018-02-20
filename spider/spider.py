from downloader.html import Html
from generators.link import Link
from file.csv import Csv
from .page import Page
import json, sys, re

# Increase stack depth
sys.setrecursionlimit(999999999)

class Spider(object):
	def __init__(self, option = {}):
		self.file_dir = option['file_dir']
		self.file_name = option['file_name']
		self.url = option['url']
		self.homepage = option['homepage']
		self.selector = option['selector']
		self.domain = option['domain'] if 'domain' in option else ''
		self.next_page = option['next_page'] if 'next_page' in option else []
		self.pagination = option['pagination'] if 'pagination' in option else {}
		self.fields = option['fields'] if 'fields' in option else []
		self.STACK_LIMIT = option['stack_limit'] if 'stack_limit' in option else 15
		self.article_data = []

	def set_url(self, url):
		self.url = url

	def get_url(self):
		return self.url

	def set_domain(self, domain):
		self.domain = domain

	def get_domain(self):
		return self.domain

	def set_next_page(self, next_page = []):
		self.next_page = next_page

	def get_next_page(self):
		return self.next_page

	def set_pagination(self, pagination):
		self.pagination = pagination

	def get_pagination(self):
		return self.pagination

	def set_pagination_type(self, pagination_type):
		self.pagination_type = pagination_type

	def get_pagination_type(self):
		return self.pagination_type

	def set_fields(self, **fields):
		self.fields = fields

	def get_fields(self):
		return self.fields

	def add_more_fields(self, **more_fields):
		for k, v in more_fields.items():
			self.fields[k] = v

	def run(self):
		'''row = []
		csv = Csv(self.file_name + '.csv')

		for field in self.fields:
			row.append(field['name'])

		csv.write(row)'''

		self.__scrap(url = self.url, selector = self.selector, fields = self.fields, pagination = self.pagination, index = (self.pagination['start'] if 'start' in self.pagination else 0))

		with open(self.file_dir + '/' + self.file_name + '.json', 'r') as f:
			data = f.read()
		with open(self.file_dir + '/' + self.file_name + '.json', 'w') as f:
			f.write('[' + data[:-1] + ']')

	def __get_html(self, url, request = {}, stack_limit = 0, type = 'GET'):
		html = Html(url, type = type, request_data = request)
		html_data = html.get_html()

		if html_data != 'error':
			return html_data
		else:
			if stack_limit >= self.STACK_LIMIT:
				print('Skipping: ' + '=' * 5 + '>' + url)
				return

			print('Retrying: ' + '-' * 5 + '>' + url)
			stack_limit += 1
			return self.__get_html(url, request, stack_limit, type = type)

	# Recursive call for url
	def __scrap(self, url = '', selector = {}, fields = [], pagination = {}, index = 0, recursion_stack = 0, request = {}, type = 'GET'):
		print(" " * (3 + 2 * recursion_stack) + "|" + "-" * (3 + 2 * recursion_stack), end = '')
		print(url)

		html_data = self.__get_html(url, request, type = type)

		if not html_data:
			return

		page = Page(html_data)
		urls = page.get_urls(selector)

		for url_i in urls:
			print(" " * (3 + 2 * recursion_stack) + "|" + "-" * (3 + 2 * recursion_stack), end = '')

			if 'relative' in selector and selector['relative']:
				url_i = self.homepage + url_i

			if recursion_stack:
				self.article_data.append(self.__scrap_article(url = url_i, fields = fields))
			else:
				self.__write_data(self.__scrap_article(url = url_i, fields = fields))

		type = 'POST' if 'type' in pagination and pagination['type'] == 'POST' else 'GET'

		index += (pagination['step'] if 'step' in pagination else 1)

		if 'pagination_key' in pagination:
			pagination = self.__resolve_pagination_key(index, pagination = pagination) or pagination

		if 'replace' in pagination:
			pagination['url'] = self.__resolve_pagination_replace(pagination['url'], pagination['replace'])

		url = self.__resolve_pagination((re.sub(re.escape(pagination['url'].replace('{page}', 'regular_expression')).replace('regular_expression', '\d+'), '', url) + pagination['url']) if 'relative' in pagination and pagination['relative'] else pagination['url'], index)

		if 'depth' in pagination and index > pagination['depth']:
			return

		if urls:
			if 'request' in pagination:
				request = pagination['request']

			self.__scrap(url = url, selector = selector, fields = fields, pagination = pagination, index = index, recursion_stack = recursion_stack, request = request, type = type)
			if recursion_stack:
				return self.article_data
		else:
			return

	def __resolve_pagination(self, url, page):
		return url.format(page = page)

	def __resolve_pagination_replace(self, url, replace = {}):
		replace['page'] = '{page}'

		return url.format(**replace)

	def __resolve_pagination_key(self, page, pagination = {}):
		if 'pagination_key' in pagination:
			if type(pagination['pagination_key']) is list:
				for pagination_key in pagination['pagination_key']:
					if 'request' in pagination and 'post_data' in pagination['request'] and pagination_key in pagination['request']['post_data']:
						pagination['request']['post_data'][pagination_key] = page
						return pagination
			else:
				if 'request' in pagination and 'post_data' in pagination['request'] and pagination['pagination_key'] in pagination['request']['post_data']:
					pagination['request']['post_data'][pagination_key] = page
					return pagination

	def __scrap_article(self, url = '', fields = [], recursion_stack = 0):
		if recursion_stack:
			print("|" , end = '')
			print(" " * (3 + 2 * recursion_stack) + "|" + "-" * (3 + 2 * recursion_stack), end = '')
			print(url)
		else:
			print(url)

		html_data = self.__get_html(url)

		if not html_data:
			return

		return self.__field_extractor(html_data = html_data, fields = fields, recursion_stack = recursion_stack)

	def __field_extractor(self, html_data = '', fields = [], recursion_stack = 0):
		field_data = {}

		page = Page(html_data)

		for field in fields:
			data_array = page.get_data(field['selector'])

			if data_array:
				if field['type'] == 'text':
					field_data[field['name']] = [data_array[i][field['selector']['attribute'] if 'attribute' in field['selector'] else 'text'] for i in range(len(data_array))]
				elif field['type'] == 'value':
					field_data[field['name']] = [data_array[i][field['selector']['attribute'] if 'attribute' in field['selector'] else 'value'] for i in range(len(data_array))]
				elif field['type'] == 'html':
					field_data[field['name']] = [data_array[i][field['selector']['attribute'] if 'attribute' in field['selector'] else 'html'] for i in range(len(data_array))]
				elif field['type'] == 'attachment':
					field_data[field['name']] = [data_array[i][field['selector']['attribute'] if 'attribute' in field['selector'] else 'href'] for i in range(len(data_array))]
				elif field['type'] == 'image':
					field_data[field['name']] = [data_array[i][field['selector']['attribute'] if 'attribute' in field['selector'] else 'src'] for i in range(len(data_array))]
				elif field['type'] == 'multiple':
					if 'fields' in field:
						field_data[field['name']] = [self.__field_extractor(data_array[i]['html'], field['fields'], recursion_stack) for i in range(len(data_array))]
				elif field['type'] == 'url':
					if 'relative' in field['selector'] and field['selector']['relative']:
						for i in range(len(data_array[:])):
							data_array[i]['href'] = self.homepage + data_array[i]['href']

					if 'fields' in field:
						recursion_stack_i = recursion_stack + 1

						if 'pagination' in field:
							field_data[field['name']] = [self.__scrap(url = data_array[i]['href'], selector = field['article_selector'], fields = field['fields'], pagination = field['pagination'], index = 0, recursion_stack = 1) for i in range(len(data_array))]
						else:
							field_data[field['name']] = [self.__scrap_article(data_array[i]['href'], fields = field['fields'], recursion_stack = recursion_stack_i) for i in range(len(data_array))]
					else:
						field_data[field['name']] = [data_array[i]['href'] for i in range(len(data_array))]

		# Done with data now return
		return field_data

	def __write_data(self, data):
		self.article_data = []

		with open(self.file_dir + '/' + self.file_name + '.json', 'a') as f:
			f.write(json.dumps(data, sort_keys = True, indent = 4))
			f.write(',')
