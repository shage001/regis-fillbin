'''
Sam Hage
Thesis
Scrapes internet for possible clue base
3/2016
'''

import urllib2

USER_AGENT = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
PAGE = 'http://crosswordtracker.com/'
PREFIX = 'browse/answers-starting-with-'
SUFFIX = '/?page='
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
OUT_FILE = 'assets/clues-NEW.txt'


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

	@param: {string} letter The letter we're scraping
	"""
	## first determine how many pages there are ##
	source = get_source( PAGE + PREFIX + letter )
	last_div_index = source.rfind( 'paginator' )
	last_div_index = source.rfind( 'paginator', 0, last_div_index - 1 )
	num_pages = int( source[ last_div_index + 11 : last_div_index + 13 ] )
	all_words = []

	## iterate over all pages ##
	for i in range ( 1, num_pages + 1 ):

		page = PAGE + PREFIX + str( letter ) + SUFFIX + str( i )
		source = get_source( page )

		## bound the source to the word boxes ##
		words_start = source.find( 'browse_box' )
		words_end = source.find( '</ul>', words_start )
		words = source[ words_start : words_end ]

		## extract each answer ##
		list_index = words.find( '<a class="answer"' )
		while list_index != -1:

			list_item_end = words.find( '</a>', list_index ) # end of entry

			entry = words[ list_index : list_item_end ]
			href = entry[ entry.find( 'href=' ) + 7 : entry.rfind( '">' ) ]
			answer = entry[ entry.rfind( '">' ) + 2 : ]
			all_words.append( ( answer, href ) )

			list_index = words.find( '<a class="answer"', list_item_end ) # start of next entry

	## get the clues for each answer ##
	for answer, href in all_words:
		get_clues_for_answer( answer, href )


def get_source( page ):
	"""
	**********************************************************************************************************************
	Returns the source code of a page

	@param: {string} page The page URL
	@return: {string} The page source
	"""
	try:
		## request the resource using boilerplate found on Stack Overflow once upon a time ##
		headers = { 'User-Agent' : USER_AGENT }
		request = urllib2.Request( page, None, headers )
		response = urllib2.urlopen( request )
		page_source = response.read()

	except:
		print( 'Resource error' )
		return

	return page_source


def get_clues_for_answer( answer, href ):
	"""
	**********************************************************************************************************************
	Given an answer and the href that links to its page, return all corresponding
	clues

	@param: {string} answer One answer
	@param: {string} href The path to the answer's page
	@return: {string[]} A list of clues for this answer
	"""
	clues = []
	


if __name__ == '__main__':
	main()
