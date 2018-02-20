from bs4 import BeautifulSoup
import types
import re

class Soup(object):
	def __init__(self, html):
		self.soup = BeautifulSoup(html, "html.parser")

	def nth_css_selector(self, selector):
		matches = re.match(r'((\.|#)\w+):nth-of-type\((\d+)\)', selector)
		if matches:
			grand_parents = self.soup.select(matches.group(1))
			parents = []
			parents.append(grand_parents[int(matches.group(3))])
			return parents
		else:
			return False

	def __negative_matches(self, selector):
		negative_matches = re.match(r'((\.|#)?.+):nth-of-type\(-(\d+)\)', selector)

		if negative_matches:
			return {'selector': negative_matches.group(1), 'index': int(negative_matches.group(3))}
		else:
			return {}

	def select(self , selector = {}):
		html_data = []

		if 'parent' in selector and 'element' in selector:
			matches = re.match(r'((\.|#).+):nth-of-type\(-?(\d+)\)', selector['parent'])

			negative_index = self.__negative_matches(selector['parent'])

			if matches:
				grand_parents = self.soup.select(matches.group(1))

				parents = []

				if int(matches.group(3)) <= len(grand_parents):
					if 'index' in negative_index and negative_index['index'] > 0 and negative_index['index'] <= len(grand_parents):
						parents.append(grand_parents[(len(grand_parents) - negative_index['index'])])
					else:
						parents.append(grand_parents[(int(matches.group(3)) - 1)])
			else:
				parents = []
				if negative_index and 'index' in negative_index:
					grand_parents = self.soup.select(negative_index['selector'])

					if negative_index['index'] > 0 and negative_index['index'] <= len(grand_parents):
						parents.append(grand_parents[(len(grand_parents) - negative_index['index'])])
				else:
					parents = self.soup.select(selector['parent'])

			if parents:
				for parent in parents:
					if type(selector['element']) is list:
						for element in selector['element']:
							datas = parent.select(element)
							if datas:
								break
					elif type(selector['element']) is str:
						datas = parent.select(selector['element'])

					if 'debug' in selector and selector['debug']:
						print(datas)

					for data in datas:
						content = ''

						for html_content in data.contents:
							content += re.sub(r'\s+', ' ', str(html_content).replace("\n", "").replace("\t", "")).strip()

						text = data.get_text()
						text = re.sub(r'\s+', ' ', text.replace("\n", "").replace("\t", "")).strip()

						if 'attribute' in selector:
							html_data.append({'text': text, 'href': data.get('href'), 'html': content, selector['attribute']: data[selector['attribute']] if selector['attribute'] in data.attrs else ''})
						else:
							html_data.append({'text': text, 'href': data.get('href'), 'html': content})
		elif 'element' in selector:
			if type(selector['element']) is list:
				for element in selector['element']:
					negative_index = self.__negative_matches(element)

					if negative_index and 'index' in negative_index:
						datas = []
						elements = self.soup.select(negative_index['selector'])

						if negative_index['index'] > 0 and negative_index['index'] <= len(elements):
							datas.append(elements[(len(elements) - negative_index['index'])])
					else:
						datas = self.soup.select(element)

					if datas:
						break
			elif type(selector['element']) is str:
				negative_index = self.__negative_matches(selector['element'])
				if negative_index and 'index' in negative_index:
					datas = []
					elements = self.soup.select(negative_index['selector'])

					if negative_index['index'] > 0 and negative_index['index'] <= len(elements):
						datas.append(elements[(len(elements) - negative_index['index'])])
				else:
					datas = self.soup.select(selector['element'])

			if 'debug' in selector and selector['debug']:
				print(datas)

			if datas:
				for data in datas:
					content = ''

					for html_content in data.contents:
						content += re.sub(r'\s+', ' ', str(html_content).replace("\n", "").replace("\t", "")).strip()

					text = data.get_text()
					text = re.sub(r'\s+', ' ', text.replace("\n", "").replace("\t", "")).strip()

					if 'attribute' in selector:
						html_data.append({'text': text, 'href': data.get('href'), 'html': content, selector['attribute']: data[selector['attribute']] if selector['attribute'] in data.attrs else ''})
					else:
						html_data.append({'text': text, 'href': data.get('href'), 'html': content})

		if 'debug' in selector and selector['debug']:
			print(html_data)

		return html_data

	def find_urls(self , selector = {}):
		hrefs = []

		if 'parent' in selector and 'element' in selector:
			parents = self.soup.select(selector['parent'])

			if parents:
				for parent in parents:
					datas = parent.select(selector['element'])

					if 'debug' in selector and selector['debug']:
						print(datas)

					hrefs.append(datas[0].get('href'))

		elif 'element' in selector:
			datas = self.soup.select(selector['element'])

			if 'debug' in selector and selector['debug']:
				print(datas)

			if datas:
				for data in datas:
					hrefs.append(data.get('href'))

		if 'debug' in selector and selector['debug']:
			print(hrefs)

		return hrefs
