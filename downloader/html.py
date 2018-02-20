import urllib.request
import json, re, requests
from socket import timeout

class Html(object):
	def __init__(self, url, type = 'GET', request_data = {}):
		self.url = url if re.match(r'https?:', url) else 'http:' + url
		self.html = self.run(type, request_data)

	def set_url(self, url):
		self.url = url

	def get_url(self):
		return self.url

	def get_html(self):
		return self.html

	def run(self, type = 'GET', request_data = {}):
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

		if 'header' in request_data:
			headers.update(request_data['header'])
			#print(headers)

		if type == 'GET':
			try:
				request = urllib.request.Request(self.url, headers = headers)
				response = urllib.request.urlopen(request, timeout = 35).read()

				if 'header' in request_data:
					if 'data' in request_data:
						if request_data['data']['type'] == 'json':
							json_response = json.loads(response.decode('utf8'))
							response = json_response[request_data['data']['selector']]

				return response
			except Exception as error:
				print('URL: {} Error: {}'.format(self.url, error))


		elif type == 'POST':			
			try:
				post_data = request_data['post_data'] if 'post_data' in request_data else {}
				
				request = urllib.request.Request(self.url, urllib.parse.urlencode(post_data).encode(), headers = headers)
				response = urllib.request.urlopen(request, timeout = 15).read()
				
				if 'header' in request_data:
					if 'data' in request_data:
						if request_data['data']['type'] == 'json':
							json_response = json.loads(response.decode('utf8'))
							response = json_response[request_data['data']['selector']]
				return response
			except Exception as error:
				print('URL: {} Error: {}'.format(self.url, error))

		return 'error'

	def login(self, login_url, form_data = {}, url = ''):
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36"}

		with requests.session() as s:
			try:
				s.post(login_url, data = payload, headers = headers)
			except Exception as error:
				print('Login Error:: URL: {} Error: {}'.format(login_url, error))

			self.session = s

			if url:
				try:
					request = s.get(url, headers = headers)
				except Exception as error:
					print('URL: {} Error: {}'.format(url, error))
