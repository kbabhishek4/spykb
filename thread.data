#override default settings
#copy this file to create multiple thread

option = {
	'url'					: 'url_to_crawl',
	'file_name'		: 'save_file_name',
	'pagination'	: {
		'url'			: 'https://www.example.com/ajax.php?search1={search1}&search2={search2}&page={page}',
		'replace'		: {
			'search1'		: 'search1_data',
			'search2'		: 'search2_data'
		},
		'start'			: 1,
		'step'			: 1,
		'request'		: {
			'header'		: {
				'cookie' 		: '',
				'referer' 		: 'https://www.example.com/',
			},
			'data'			: {
				'type'			: 'json',
				'selector'		: 'markup'
			}
		}
	}
}
