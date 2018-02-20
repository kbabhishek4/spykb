import threading
from spider.spider import Spider

class Sthread(threading.Thread):
	def __init__(self, thread_id, name, option = {}):
		threading.Thread.__init__(self)
		self.thread_id = thread_id
		self.name = name
		self.option = option
	
	def run(self):
		#getattr(globals()['class_name'](), 'function_name')('args')
		print('-|' * 5 + 'Starting ' + self.name + ' Thread ID:: ' + str(self.thread_id))
		spider = Spider(self.option)
		spider.run()