'''
Sam Hage
Script to take data from clue database and put it in the format I want
11/205
'''

import re

SPACE_BUFFER = '    ' # element found on almost line between clue and answer
ORIGINAL_FILE = 'assets/clues.txt'
NEW_FILE = 'assets/clues-good.txt'

def main():
	"""
	**********************************************************************************************************************
	Main code to run on program execution
	"""
	## commented out so I don't accidentally wipe my data ##
	# remove_unnecessary_info()
	# sort_answers()


def remove_unnecessary_info():
	"""
	**********************************************************************************************************************
	Preserve only the clue and answer from the data
	"""
	orig = open( ORIGINAL_FILE, 'r' )
	new = open( NEW_FILE, 'w' )

	for line in orig:
		start_of_garbage = line.rfind( SPACE_BUFFER ) + 4
		end_of_garbage = start_of_garbage + 10
		new_line = line[ : start_of_garbage ] + line[ end_of_garbage : ]
		new.write( new_line )

	orig.close()
	new.close()


def sort_answers():
	"""
	**********************************************************************************************************************
	Store the clues and answers as tuples, switch their order, then flip them
	"""
	orig = open( NEW_FILE, 'r' )
	unsorted_pairs = []
	non_white_space = re.compile( '[^\s]' )

	## grab clue answer pair ##
	for line in orig:
		end_of_answer = line.find( '  ' )
		answer = line[ : end_of_answer ]
		line = line[ end_of_answer : ]

		find_non_white = re.search( non_white_space, line )
		if find_non_white:
			start_of_clue = find_non_white.start()
			clue = line[ start_of_clue : ].strip()
			pair = ( clue, answer )
			unsorted_pairs.append( pair )
		else:
			print( line )

	orig.close()

	## sort the pairs alphabetically by clue and remove duplicates ##
	sorted_pairs = sorted( list( set( unsorted_pairs ) ) )

	## write the sorted pairs back out ##
	new = open( NEW_FILE, 'w' )

	for pair in sorted_pairs:
		new_line = str( pair ) + '\n'
		new.write( new_line )

	new.close()


if __name__ == '__main__':
	main()
