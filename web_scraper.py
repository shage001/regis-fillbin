'''
Sam Hage
Thesis
Scrapes internet for possible clue base
3/2016
'''

import urllib2

USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
PREFIX = 'http://crosswordtracker.com/browse/answers-starting-with-'
SUFFIX = '/?page='
ANSWER_PAGE = 'http://crosswordtracker.com/answer/'


def main():
	"""
	**********************************************************************************************************************

	"""

def get_source( page ):
	"""
	**********************************************************************************************************************

	"""
	try:
		## request the resource using boilerplate found on Stack Overflow once upon a time ##
		headers = { 'User-Agent' : USER_AGENT }
		request = urllib2.Request( page, None, headers )
		response = urllib2.urlopen( request )
		page_source = response.read()

	except:
		print( 'Resource error' )

	return page_source


if __name__ == '__main__':
	main()
