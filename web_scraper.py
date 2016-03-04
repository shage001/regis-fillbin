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
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def main():
	"""
	**********************************************************************************************************************
	Main function to run on program execution
	"""
	# scrape_all_data()
	scrape_single_letter( 'a' )


def scrape_all_data():
	"""
	**********************************************************************************************************************
	Goes through all 26 letters to scrape the data
	"""
	for letter in ALPHABET:
		scrape_single_letter( letter )


def scrape_single_letter( letter ):
	"""
	**********************************************************************************************************************
	Scrapes data for a single letter
	"""
	## first determine how many pages there are ##
	source = get_source( PREFIX + letter )
	last_div_index = source.rfind( 'paginator' )
	last_div_index = source.rfind( 'paginator', 0, last_div_index - 1 )
	num_pages = source[ last_div_index + 11 : last_div_index + 13 ]

	## iterate over all pages ##
	for i in range ( 1, num_pages + 1 ):
		page = PREFIX + letter + SUFFIX + i
		source = get_source( page )


def get_source( page ):
	"""
	**********************************************************************************************************************
	Returns the source code of a page

	@param: {string} page The page URL
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


def get_clues_for_answer( answer, href ):
	"""
	**********************************************************************************************************************
	Given an answer and the href that links to its page, return all corresponding
	clues
	"""


if __name__ == '__main__':
	main()
