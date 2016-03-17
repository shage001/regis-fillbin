'''
Sam Hage
Thesis
Used to get potential answers for clues
12/2015
'''

# NOTE to future Sam: big win possible from using crosswordtracker scraped
# data instead of current

import string
import sys
import ast
import re
import random
import puzzle_structure
import manipulate_clues

LONG_FILE_PATH = 'assets/clues-NEWEST.txt'
FILE_PATH_3 = 'assets/clues-3.txt'
FILE_PATH_4 = 'assets/clues-4.txt'
FILE_PATH_5 = 'assets/clues-5.txt'
FILE_PATH_6 = 'assets/clues-6.txt'
FILE_PATH_7 = 'assets/clues-7+.txt'
# SHORT_FILE_PATH = 'assets/clues-short.txt'
WORDS_FILE = 'assets/words-answers.txt'
WIKI_FILE = 'assets/wiki-titles-2.txt'
# SHORTENING_FACTOR = 1
TO_IGNORE = [ 'the', 'a', 'an', 'of', 'with', 'and', 'in' ]
MIN_DISTANCE = 5

def main():
	"""
	**********************************************************************************************************************
	Main code to be run at program execution
	"""
	# pairs = load_clues( CLUES_FILE_PATH )
	puzzle_name = 'oct0515'
	puzzle_structure.read_raw_puzzle( puzzle_name )
	lookup_all_clues( puzzle_name )


def strip_puzzle_name( str ):
	"""
	**********************************************************************************************************************
	Makes sure the puzzle name is in the right format

	@param: {string} str The name of the puzzle
	"""
	## strip file extension ##
	str.replace( '.txt', '' );
	## check for proper format ##
	if '/' in str:
		raise Exception( 'Incorrect format for puzzle_name. Should be monDDYY.' )
	## return puzzle name ##
	return str


def lookup_all_clues( puzzle_name ):
	"""
	**********************************************************************************************************************
	Look up all the clues for potential answers. Uses binary search and fuzzy search

	@param: {string} puzzle_name
	"""
	## load long list of clues into memory ##
	print( 'Loading clues...' )
	long_pairs = load_clues( LONG_FILE_PATH )
	pairs_3 = load_clues( FILE_PATH_3 )
	pairs_4 = load_clues( FILE_PATH_4 )
	pairs_5 = load_clues( FILE_PATH_5 )
	pairs_6 = load_clues( FILE_PATH_6 )
	pairs_7 = load_clues( FILE_PATH_7 )
	print( 'Done.' )
	## randomly shorten the list and load those as well ##
	# shorten_clues( SHORTENING_FACTOR )
	# short_pairs = load_clues( SHORT_FILE_PATH )

	## read current answers from answers.txt ##
	puzzle_name = strip_puzzle_name( puzzle_name )

	with open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt' ) as f:
		lines = f.read().splitlines()
	num_clues = len( lines ) - 3
	i = 0
	j = -1

	out_file = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'w' )

	out_file.write( '----------------------------------------------------\n')
	out_file.write( 'i\tj\tA/D\t\t[clue, pattern]\t\t\t\tanswers\n')
	out_file.write( '----------------------------------------------------\n')
	message = 'Computing answers'
	for line in lines:
		j += 1
		if ( j < 3 ):
			continue

		## parse the lines and look up the answers for each clue ##
		info = line.split( '\t' )
		clue = ast.literal_eval( info[3] )[0]
		pattern = ast.literal_eval( info[3] )[1]

		## figure out which list of shorter clues to use ##
		if len( pattern ) == 3:
			short_pairs = pairs_3
		elif len( pattern ) == 4:
			short_pairs = pairs_4
		elif len( pattern ) == 5:
			short_pairs = pairs_5
		elif len( pattern ) == 6:
			short_pairs = pairs_6
		else:
			short_pairs = pairs_7

		answers = lookup_single_clue( clue, pattern, long_pairs, short_pairs )
		out_file.write( info[0] + '\t' + info[1] + '\t' + info[2] + '\t' + str( info[3] ) + '\t' + str( answers ) + '\n' )

		sys.stdout.write( '\r                                ' )
		sys.stdout.write( '\r' + message + ( i % 4 )*'.' + ( 5 - i % 4 )*' ' + str( i + 1 ) + '/' + str( num_clues ) )
		sys.stdout.flush()
		i += 1

	out_file.close()
	print( '\nDone.' )


def lookup_single_clue( clue, pattern, long_pairs, short_pairs ):
	"""
	**********************************************************************************************************************
	Get a list of answers for a single clue based on the clue and pattern. Uses
	binary search and fuzzy search.

	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} long_pairs The clue/answer data
	@param: {string[]} short_pairs The clue/answer data partitioned by length
	@return: {string[]} A list of possible answers
	"""
	## try binary search, otherwise use fuzzy ##
	answers = binary_search( clue, pattern, long_pairs )
	if len( answers ) == 0:
		answers = fuzzy_search( clue, pattern, short_pairs )

	return answers


def binary_search( clue, pattern, pairs ):
	"""
	**********************************************************************************************************************
	Perform standard binary search with incorporation of minimum edit distance

	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} pairs The clue/answer data
	@return: {string[]} A list of possible answers
	"""
	clue = clue.lower()
	floor = 0
	ceiling = len( pairs ) - 1
	answers = []

	while floor <= ceiling:
		middle = ( floor + ceiling ) // 2
		cur_pair = ast.literal_eval( pairs[middle] )
		cur_clue = cur_pair[0].lower()
		if cur_clue > clue:
			ceiling = middle - 1
		elif cur_clue < clue:
			floor = middle + 1
		else:
			if len( cur_pair[1] ) == len( pattern ):
				answers = [ cur_pair[1] ]
			break
	if manipulate_clues.minimum_edit_distance( cur_clue, clue ) < MIN_DISTANCE and len( cur_pair[1] ) == len( pattern ):
		answers = [ cur_pair[1] ]
	return answers


def fuzzy_search( clue, pattern, pairs ):
	"""
	**********************************************************************************************************************
	Perform a fuzzy regex search on the data. This is much slower than binary search

	@param: {string} clue
	@param: {string} pattern The answer pattern so far
	@param: {string[]} pairs The clue/answer data
	@return: {string[]} A list of possible answers
	"""
	answers = []
	key_words = clue.split()
	## extract key words ##
	key_words = [ word.strip( string.punctuation ) for word in key_words if word not in TO_IGNORE ]

	# TODO: try using 'all' intead of regex per http://stackoverflow.com/questions/11190835/regular-expressions-in-python-unexpectedly-slow
	# e.g. 		if all( word in item for word in key_words):

	## find answers that have a reasonable match with the clue ##
	for i, item in enumerate( pairs ):
		num_matches = 0
		num_missed = 0
		for word in key_words:
			if re.search( word, item, re.IGNORECASE ):
				num_matches += 1
			else:
				num_missed += 1
			if num_missed > len( key_words ) // 2:
				break

		if float( num_matches ) / len( key_words ) > .5:
			answer = ast.literal_eval( item )[1]
			if len( answer ) == len( pattern ) and answer not in answers:
				answers.append( answer )

	return answers


def single_word_match( pattern ):
	"""
	**********************************************************************************************************************
	Match a single word by letter pattern from a word list

	@param: {string} pattern Pattern of letters and question marks
	@return: {string[]} A list of possible word matches
	"""
	f = open( WORDS_FILE, 'r' )
	words = f.read().splitlines()
	# num_blanks = pattern.count( '?' )
	to_search = pattern.lower()
	to_search = re.compile( to_search.replace( '?', '.' ) )
	possible_matches = [ word.upper() for word in words if re.search( to_search, word.lower() ) \
	 					 and len( word ) == len( pattern ) ]
	return possible_matches


def wiki_title_match( pattern ):
	"""
	**********************************************************************************************************************
	Match a single clue by letter pattern from a list of wikipedia titles

	@param: {string} pattern Pattern of letters and question marks
	@return: {string[]} A list of possible word matches
	"""
	f = open( WIKI_FILE, 'r' )
	titles = f.read().splitlines()
	# num_blanks = pattern.count( '?' )
	to_search = pattern.lower()
	to_search = re.compile( to_search.replace( '?', '.' ) )
	possible_matches = [ title for title in titles if re.search( to_search, title.lower() ) \
	 					 and len( title ) == len( pattern ) ]
	return possible_matches


def shorten_clues( factor ):
	"""
	**********************************************************************************************************************
	Randomly shorten the input list by some factor and write new list to clues-short.txt

	@param: {int} factor The factor to shorten by
	"""
	message = 'Compressing data'
	long_pairs = load_clues( LONG_FILE_PATH )
	num_pairs = len( long_pairs )
	short_pairs = []
	i = 0
	for pair in long_pairs:
		rand = random.randint( 0, factor - 1 )
		if rand == 0:
			short_pairs.append( pair )

		percent = ( float(i) / num_pairs ) * 100.0
		sys.stdout.flush()
		sys.stdout.write( '\r                                ' )
		sys.stdout.write( '\r' + message + ( (i//50000) % 4 )*'.' + ( 5 - (i//50000) % 4 )*' ' + str( int( percent ) ) + '%'  )
		i += 1
	print( '\nDone.')

	short_clue_file = open( SHORT_FILE_PATH, 'w' )
	for pair in short_pairs:
		short_clue_file.write( pair + '\n' )
	short_clue_file.close()


def load_clues( file_path ):
	"""
	**********************************************************************************************************************
	Load the clue/answer data into memory

	@param: {string} file_path
	@return: {string[]} The clue/answer data
	"""
	clue_file = open( file_path, 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	return pairs


if __name__ == '__main__':
	main()
