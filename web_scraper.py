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
## CHANGE BACK!!!!! ##
ALPHABET = 'wxyz'
NUMBERS = '0123456789'
OUT_FILE = 'assets/clues-NEW3.txt'


def main():
	"""
	**********************************************************************************************************************
	Main function to run on program execution
	"""
	scrape_all_data()
	# scrape_single_letter( 'b' )


def scrape_all_data():
	"""
	**********************************************************************************************************************
	Goes through all 26 letters to scrape the data
	"""
	for letter in ALPHABET:
		print( letter )
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

	if source[ last_div_index + 12 : last_div_index + 13 ] in NUMBERS: # single v double digit pages
		num_pages = int( source[ last_div_index + 11 : last_div_index + 13 ] )
	else:
		num_pages = int( source[ last_div_index + 11 : last_div_index + 12 ] )

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
	out_file = open( OUT_FILE, 'a' )

	for answer, href in all_words:
		clues = get_clues_for_answer( answer, href )
		for clue in clues:
			out_file.write( '(' + clue + ', ' + answer + ')\n' )

	out_file.close()


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
	all_clues = []
	source = get_source( PAGE + href )
	if not source: # skip broken links that came up in some tests
		print( 'Broken link for ' + str( ( answer, href ) ) )
		return all_clues

	clues_start = source.find( 'sortable clue-list' )
	clues_end = source.find( '</div>', clues_start )
	clues = source[ clues_start : clues_end ]

	list_index = clues.find( 'data-count="' )
	while list_index != -1:

		list_item_end = clues.find( '</a>', list_index )

		clue = clues[ clues.find( '">', list_index + 18 ) + 2 : list_item_end ]
		all_clues.append( clue )
		# print( clue, answer )

		list_index = clues.find( 'data-count="', list_item_end )

	return all_clues


if __name__ == '__main__':
	main()
