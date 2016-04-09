'''
Sam Hage
Thesis
Driver for the puzzle solver.
12/2015

TODO:
- improve performance with uncompressed data X
- improve performance with custom scraped data X
- partition data based on answer length X
- partition wiki data X
- improve binary search to check surrounding answers
- add wikipedia search

LIMITATIONS:
- wordplay/humor
- in-puzzle references
- multiple letters per square / non-alphanumeric characters
- rich text (accents, etc)
'''

import sys
import puzzle_solver
import evaluate

WEEK = [ 'oct0906', 'dec2899', 'jun0497', 'nov0515', 'nov0615', 'apr2796', 'nov0815' ]

def main():
	"""
	**********************************************************************************************************************
	Run on file execution
	"""
	# puzzle_name = WEEK[3]
	# puzzle_name = 'oct0515'
	# puzzle_name = 'dec3014'
	puzzle_name = 'jan2710'
	puzzle_solver.fill( puzzle_name )
	diff = evaluate.compare_results( puzzle_name )
	evaluate.score_puzzle( diff )


if __name__ == '__main__':
	main()
