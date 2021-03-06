'''
Sam Hage
Thesis
A bunch of hacky functions to manipulate the crossword data. Most were used once
to preprocess the data. DON'T RUN THESE.
12/2015
'''

import ast
import string
import re

TO_IGNORE = [ 'the', 'a', 'an', 'of', 'with', 'and', 'in' ]

def to_lower():
	"""
	**********************************************************************************************************************
	turn all clues to lower case
	"""
	clue_file = open( 'assets/clues-good.txt', 'r' )
	new_clue_file = open( 'assets/clues-better.txt', 'w' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	for pair in pairs:
		pair = ast.literal_eval( pair )
		lower_pair = ( pair[0].lower(), pair[1] )
		new_clue_file.write( str( lower_pair ) + '\n' )

	new_clue_file.close()

def re_sort():
	"""
	**********************************************************************************************************************
	need to resort now that clues are lower case
	"""
	clue_file = open( 'assets/clues-better.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	new_clue_file = open( 'assets/clues-better.txt', 'w' )
	for pair in pairs:
		new_clue_file.write( str( pair )[2:] + '\n' )
	new_clue_file.close()

	clue_file = open( 'assets/clues-better.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	sorted_pairs = sorted( list( set( pairs ) ) )
	new_clue_file = open( 'assets/clues-better.txt', 'w' )
	for pair in sorted_pairs:
		new_clue_file.write( str( pair ) + '\n' )
	new_clue_file.close()


def match_quotes():
	"""
	**********************************************************************************************************************
	re-append the opening paren and either single or double quote
	"""
	clue_file = open( 'assets/clues-better.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()
	new_clue_file = open( 'assets/clues-better.txt', 'w' )
	for pair in pairs:
		capital_index = 0
		for letter in pair:
			if letter.isupper():
				break
			else:
				capital_index += 1
		quote = pair[ capital_index - 4 ]
		pair = '(' + quote + pair
		new_clue_file.write( pair + '\n' )

	new_clue_file.close()


def make_key_word_list():
	"""
	**********************************************************************************************************************
	generate a new list of just key words
	"""
	clue_file = open( 'assets/clues-better.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()

	new_clue_file = open( 'assets/clues-key-words.txt', 'w' )
	for pair in pairs:
		key_words = [ word.strip( string.punctuation + ' ' ) \
			for word in ast.literal_eval( pair )[0].split() \
			if word.strip( string.punctuation + ' ' ) not in TO_IGNORE ]
		key_string = ' '.join( key_words )
		new_tuple = ( key_string.strip(), ast.literal_eval( pair )[1] )
		new_clue_file.write( str( new_tuple ) + '\n' )

	new_clue_file.close()


def shorten_list():
	"""
	**********************************************************************************************************************
	remove clues that are too long
	"""
	clue_file = open( 'assets/clues-better.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()

	new_clue_file = open( 'assets/clues-best.txt', 'w' )
	for pair in pairs:
		clue = ast.literal_eval( pair )[0]
		if len( clue ) <= 75:
			new_clue_file.write( pair + '\n' )

	new_clue_file.close()

def shorten_list_2():
	"""
	**********************************************************************************************************************
	remove clues based on min edit distance

	this DOES NOT WORK
	"""
	clue_file = open( 'assets/clues-best.txt', 'r' )
	pairs = clue_file.read().splitlines()
	clue_file.close()

	final_pairs = []
	j = 1
	for pair in pairs:
		print( j )
		j += 1
		clue1 = ast.literal_eval( pair )[0]
		answer1 = ast.literal_eval( pair )[1]
		duplicate = False
		for final_pair in final_pairs:
			clue2 = ast.literal_eval( final_pair )[0]
			answer2 = ast.literal_eval( final_pair )[1]
			edit_distance = minimum_edit_distance( clue1, clue2 )
			if edit_distance < 10 and clue1 == clue2:
				# print( 'duplicate' )
				duplicate = True
				break
		if not duplicate:
			final_pairs.append( pair )
			# print( 'no duplicate' )

	new_clue_file = open( 'assets/clues-bestest.txt', 'w' )
	for pair in final_pairs:
		new_clue_file.write( pair + '\n' )

	new_clue_file.close()


def parse_wiki_titles():
	"""
	**********************************************************************************************************************
	lower case the titles and remove underscores
	(edit: and other non-alphas)
	"""
	f = open( 'assets/wiki-titles-2.txt', 'r' )
	titles = f.read().splitlines()
	f.close()
	regex = re.compile( '[^a-zA-Z]' )
	new_titles_file = open( 'assets/wiki-titles-3.txt', 'w' )
	for title in titles:
		new_title = regex.sub( '', title )
		new_titles_file.write( new_title.upper() + '\n' )

	new_titles_file.close()


def generate_dictionary():
	"""
	**********************************************************************************************************************
	create a new dictionary from only the unique answers
	"""
	f = open( 'assets/clues-best.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()
	answers = []
	for pair in pairs:
		capital_index = 0
		for letter in pair:
			if letter.isupper():
				break
			else:
				capital_index += 1
		answers.append( pair[ capital_index : pair.find( '\'', capital_index ) ] )
	answers = list( set( answers ) )
	word_file = open( 'assets/words-answers.txt', 'w' )
	for answer in answers:
		word_file.write( answer + '\n' )
	word_file.close()




def minimum_edit_distance( s1, s2 ):
	"""
	**********************************************************************************************************************
	compute the minimum edit distance between two strings
	"""
	if len(s1) > len(s2):
	    s1,s2 = s2,s1
	distances = range(len(s1) + 1)
	for index2,char2 in enumerate(s2):
		newDistances = [index2+1]
		for index1,char1 in enumerate(s1):
		    if char1 == char2:
		        newDistances.append(distances[index1])
		    else:
		        newDistances.append(1 + min((distances[index1],
		                                     distances[index1+1],
		                                     newDistances[-1])))
		distances = newDistances
	return distances[-1]


def partition_data():
	"""
	**********************************************************************************************************************
	partition data by answer length
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()
	length_pairs = [ [], [], [], [], [] ]

	for pair in pairs:
		answer = pair[ pair.rfind( ',' ) + 3 : pair.find( ')' ) - 1 ]
		if len( answer ) > 6:
			length_pairs[4].append( pair )
		else:
			length_pairs[len( answer ) - 3].append( pair )

	pairs_3 = length_pairs[0]
	pairs_4 = length_pairs[1]
	pairs_5 = length_pairs[2]
	pairs_6 = length_pairs[3]
	pairs_long = length_pairs[4]

	three_file = open( 'assets/clues-3.txt', 'w' )
	four_file = open( 'assets/clues-4.txt', 'w' )
	five_file = open( 'assets/clues-5.txt', 'w' )
	six_file = open( 'assets/clues-6.txt', 'w' )
	long_file = open( 'assets/clues-7+.txt', 'w' )

	for pair in pairs_3:
		three_file.write( pair + '\n' )

	for pair in pairs_4:
		four_file.write( pair + '\n' )

	for pair in pairs_5:
		five_file.write( pair + '\n' )

	for pair in pairs_6:
		six_file.write( pair + '\n' )

	for pair in pairs_long:
		long_file.write( pair + '\n' )

	three_file.close()
	four_file.close()
	five_file.close()
	six_file.close()
	long_file.close()


def parse_symbols():
	"""
	**********************************************************************************************************************
	replace html character codes with actual characters
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	length = len( pairs )
	for i in range( length ):
		pairs[i] = pairs[i].replace( '&quot;', '"' )
		pairs[i] = pairs[i].replace( '&#39;', '\'' )
		pairs[i] = pairs[i].replace( '&amp;', '&' )
		pairs[i] = pairs[i].replace( '&lt;', '<' )
		pairs[i] = pairs[i].replace( '&gt;', '>' )

	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in pairs:
		f.write( pair + '\n' )
	f.close()


def remove_shorts():
	"""
	**********************************************************************************************************************
	remove answers that are too short for NYT puzzle (under 3)
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	new_pairs = []
	for pair in pairs:
		print( pair )
		answer = ast.literal_eval( pair )[1]
		if len( answer ) > 2:
			new_pairs.append( pair )


	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in new_pairs:
		f.write( pair + '\n' )
	f.close()


def stringify():
	"""
	**********************************************************************************************************************
	make string lines into string tuples so literal_eval will work on them
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	length = len( pairs )
	for i in range( length ):
		clue_end = pairs[i].rfind( ',' )
		pairs[i] = pairs[i][0] + '\'' + \
				   pairs[i][ 1 : clue_end ].lower().replace( '\'', '\\\'' ) + '\', \'' + \
				   pairs[i][ clue_end + 2 : -1 ] + '\')'

	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in pairs:
		f.write( pair + '\n' )
	f.close()


def close_parens():
	"""
	**********************************************************************************************************************
	one-time paren matching fix
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	length = len( pairs )
	for i in range( length ):
		pairs[i] = pairs[i][ : -1 ]

	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in pairs:
		f.write( pair + '\n' )
	f.close()


def standardize_blanks():
	"""
	**********************************************************************************************************************
	make all word blanks three underscores (by running repeatedly)
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	length = len( pairs )
	for i in range( length ):
		pairs[i] = pairs[i].replace( '____', '___' )

	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in pairs:
		f.write( pair + '\n' )
	f.close()


def remove_non_letters():
	"""
	**********************************************************************************************************************
	throw out answers that have non-letter characters
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	new_pairs = []

	for pair in pairs:
		include = ast.literal_eval( pair )[1].isalpha()
		if include:
			new_pairs.append( pair )


	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in new_pairs:
		f.write( pair + '\n' )
	f.close()


def re_sort2():
	"""
	**********************************************************************************************************************
	sort the data in a not stupid way
	"""
	f = open( 'assets/clues-NEWEST.txt', 'r' )
	pairs = f.read().splitlines()
	f.close()

	new_pairs = sorted( pairs, cmp=compare )

	f = open( 'assets/clues-NEWEST.txt', 'w' )
	for pair in new_pairs:
		f.write( pair + '\n' )
	f.close()


def compare( a, b ):
	"""
	**********************************************************************************************************************
	custom compare function to sort clue, answer tuples
	"""
	if ast.literal_eval( a )[0] < ast.literal_eval( b )[0]:
		return -1
	elif ast.literal_eval( a )[0] == ast.literal_eval( b )[0]:
		return 0
	else:
		return 1


def partition_wiki_titles():
	"""
	**********************************************************************************************************************
	lower case the titles and remove underscores
	"""
	f = open( 'assets/wiki-titles-3.txt', 'r' )
	titles = f.read().splitlines()
	f.close()
	length_titles = [ [], [], [], [], [] ]

	for title in titles:
		if len( title ) < 3 or len( title ) > 15:
			pass
		elif len( title ) > 6:
			length_titles[4].append( title )
		else:
			length_titles[len( title ) - 3].append( title )

	titles_3 = length_titles[0]
	titles_4 = length_titles[1]
	titles_5 = length_titles[2]
	titles_6 = length_titles[3]
	titles_long = length_titles[4]

	three_file = open( 'assets/wiki-3.txt', 'w' )
	four_file = open( 'assets/wiki-4.txt', 'w' )
	five_file = open( 'assets/wiki-5.txt', 'w' )
	six_file = open( 'assets/wiki-6.txt', 'w' )
	long_file = open( 'assets/wiki-7+.txt', 'w' )

	for title in titles_3:
		three_file.write( title + '\n' )

	for title in titles_4:
		four_file.write( title + '\n' )

	for title in titles_5:
		five_file.write( title + '\n' )

	for title in titles_6:
		six_file.write( title + '\n' )

	for title in titles_long:
		long_file.write( title + '\n' )

	three_file.close()
	four_file.close()
	five_file.close()
	six_file.close()
	long_file.close()


if __name__ == '__main__':
	# parse_wiki_titles()
	# partition_wiki_titles()
	pass
