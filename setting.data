option = {
	'url'					: 'url_to_crawl', #starting url of a website
	'file_name'		: 'project_file_name', #file name to save json data
	'file_dir'    : 'projects/project_name/saved', #replace project name with ur project name
	'homepage'		: 'https://www.example.com', #homepage of the website
	'selector'		: {
		'parent'		: '.cntanr', #specify the parent selector
		'element'		: '.jcn > a' #specify the child selector
	},
	'pagination'	: {
		'url'			: 'https://www.example.com/ajax.php?search1={search1}&search2={search2}&page={page}', #pagination url for the next page to crawl
		'replace'		: {
			'search1'		: 'search1_data', #replace data in pagination url
			'search2'		: 'search2_data' #replace data in pagination url
		},
		'start'			: 1, #Starting page index
		'step'			: 1, #Step to increase page index
		'request'		: {
			'header'		: { #optional for few sites
				'cookie' 		: '',
				'referer' 		: 'https://www.example.com/',
			},
			'data'			: { #optional for few sites
				'type'			: 'json',
				'selector'		: 'markup'
			}
		}
	},
	'fields'		: [{ #specify fields for extracting data from the article page
		'name'			: 'MetaTitle',
		'type'			: 'text',
		'selector'		: {
			'element'		: 'title'
		}
	}, {
		'name'			: 'MetaDescription',
		'type'			: 'text',
		'selector'		: {
			'element'		: 'meta[name="description"]',
			'attribute'		: 'content',
		}
	}, {
		'name'			: 'Image',
		'type'			: 'text',
		'selector'		: {
			'element'		: 'meta[property="og:image"]',
			'attribute'		: 'content',
		}
	}, {
		'name'			: 'Gallery',
		'type'			: 'text',
		'selector'		: {
			'parent'		: '#gal_img',
			'element'		: 'a',
			'attribute'		: 'data-original',
		}
	}, {
		'name'			: 'Title',
		'type'			: 'text',
		'selector'		: {
			'parent'		: 'h1',
			'element'		: '.fn'
		}
	}, {
		'name'			: 'Telephone',
		'type'			: 'text',
		'selector'		: {
			'parent'		: '#comp-contact',
			'element'		: '.telCntct > a.tel'
		}
	}, {
		'name'			: 'Mobile',
		'type'			: 'text',
		'selector'		: {
			'parent'		: '#mob_set',
			'element'		: '.telCntct'
		}
	}, {
		'name'			: 'Address',
		'type'			: 'text',
		'selector'		: {
			'element'		: '#fulladdress > span'
		}
	}, {
		'name'			: 'YearEstablished',
		'type'			: 'text',
		'selector'		: {
			'parent'		: '.alstdul:nth-of-type(-1)',
			'element'		: 'li'
		}
	}, {
		'name'			: 'Website',
		'type'			: 'text',
		'selector'		: {
			'parent'		: '.mreinfp:nth-of-type(1)',
			'element'		: 'a',
			'attribute'		: 'title'
		}
	}, {
		'name'			: 'Business Info',
		'type'			: 'multiple',
		'selector'		: {
			'element'		: '.businfo '
		},
		'fields'		: [{
			'name'			: 'Business Information',
			'type'			: 'text',
			'selector'		: {
				'element'		: '.detl'
			}
		}, {
			'name'			: 'Service Offered',
			'type'			: 'text',
			'selector'		: {
				'element'		: 'p:nth-of-type(-1)',
			}
		}]
	}, {
		'name'			: 'OperationTiming',
		'type'			: 'multiple',
		'selector'		: {
			'parent'		: '#statHr',
			'element'		: '.mreinfli'
		},
		'fields'		: [{
			'name'			: 'Day',
			'type'			: 'text',
			'selector'		: {
				'element'		: '.mreinflispn1'
			}
		}, {
			'name'			: 'Time',
			'type'			: 'text',
			'selector'		: {
				'element'		: '.mreinflispn2'
			}
		}]
	}, {
		'name'			: 'Rating',
		'type'			: 'multiple',
		'selector'		: {
			'element'		: '.rtngsval'
		},
		'fields'		: [{
			'name'			: 'Votes',
			'type'			: 'text',
			'selector'		: {
				'element'		: '.votes'
			}
		}, {
			'name'			: 'Rating',
			'type'			: 'text',
			'selector'		: {
				'element'		: '.value-title',
				'attribute'		: 'title'
			}
		}]
	}]
}
