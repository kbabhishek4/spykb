from spider.spider import Spider
from library.sthread import Sthread
import glob, sys, os, shutil

SETTING_FILE = 'projects/{project_name}/threads/*.py'
COMMON_SETTING_FILE = 'projects/{project_name}/{project_name}_common_setting.py'

if __name__ == "__main__":
	if len(sys.argv) < 3 or sys.argv[1].lower() == 'help':
		print("\n")
		print('*' * 60)
		print("""
		Please enter the options as followed
		create project_name
		start project_name
		""")
		print('*' * 60)
		print("\n")
		sys.exit(2)

	if sys.argv[1] == 'create':
		if not os.path.exists('projects/' + sys.argv[2] + '/threads') and not os.path.exists('projects/' + sys.argv[2] + '/saved'):
			os.makedirs('projects/' + sys.argv[2] + '/threads')
			os.makedirs('projects/' + sys.argv[2] + '/saved')
			shutil.copy2('thread.data', 'projects/' + sys.argv[2] + '/threads/'+ sys.argv[2] + '_thread_1.py')
			shutil.copy2('setting.data', 'projects/' + sys.argv[2] + '/'+ sys.argv[2] + '_common_setting.py')
			print("\n")
			print('*' * 60)
			print("""
		project {project_name} created successfully,
		define multiple setting threads under projects/{project_name}/threads,
		your output will be under projects/{project_name}/saved
			""".format(project_name = sys.argv[2]))
			print('*' * 60)
			print("\n")

	if sys.argv[1] == 'start':
		options = []
		common_option = __import__(COMMON_SETTING_FILE.format(project_name = sys.argv[2]).replace('/', '.').replace('\\', '.')[:-3], globals(), locals(), ['option']).option

		setting_files = glob.glob(SETTING_FILE.format(project_name = sys.argv[2]))

		for setting_file in setting_files:
			common_option.update(__import__(setting_file.replace('/', '.').replace('\\', '.')[:-3], globals(), locals(), ['option']).option)
			options.append(common_option.copy())

		if len(options) > 1:
			thread_list = [Sthread(thread_id = i , name = options[i]['site_name'] , option = options[i]) for i in range(len(options))]

			for thread in thread_list:
				thread.start()
		else:
			spider = Spider(options[0])
			spider.run()
