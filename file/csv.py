import csv
import types

class Csv(object):
	def __init__(self, file):
		self.file = file
		
	def write(self, content):
		with open(self.file, 'a', newline = '') as csv_file:
			csv_writer = csv.writer(csv_file, delimiter = ',')
			if type(content) is list:
				csv_writer.writerows(','.join(content))
			elif type(content) is str:
				csv_writer.writerow(content)
	
	