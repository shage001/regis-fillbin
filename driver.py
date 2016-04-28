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

import os
import sys
import puzzle_solver
import evaluate

WEEK = [ 'oct0906', 'dec2899', 'jun0497', 'nov0515', 'nov0615', 'apr2796', 'nov0815' ]

def main():
	"""
	**********************************************************************************************************************
	Run on file execution
	"""

	args = sys.argv
	downloads = False
	allPuzzles = False

	if len( args ) == 1: # no flags
		pass
	elif args[1] == '-d' or args[1] == '--downloads':
		downloads = True
	elif args[1] == '-a' or args[1] == '--all':
		allPuzzles = True

	if downloads: # pull latest puzzle from downloads

		## parse the puzzle out of downloads ##
		os.system( './single_parser.rb' )
		with open( 'log.txt', 'r' ) as log_file:
			puzzle_name = log_file.readline()
		log_file.close()

		## solve the puzzle ##
		puzzle_solver.fill( puzzle_name )
		diff = evaluate.compare_results( puzzle_name )
		evaluate.score_puzzle( diff )

	elif allPuzzles: # test all puzzles
		## record puzzles done so far ##
		with open( 'done.txt', 'r' ) as done_file:
			done = done_file.read().splitlines()
		done_file.close()


		for puzzle_name in os.listdir( 'puzzles/' ):

			## avoid hidden files and previously solved ones ##
			if len( puzzle_name ) != 7 or puzzle_name in done:
				continue
			puzzle_solver.fill( puzzle_name )
			diff = evaluate.compare_results( puzzle_name )
			evaluate.score_puzzle( diff )
			with open( 'done.txt', 'a' ) as done_file:
				done_file.write( puzzle_name + '\n' )
			done_file.close()

	else: # do a single puzzle
		# puzzle_name = WEEK[0]
		# puzzle_name = 'oct0515'
		# puzzle_name = 'dec3014'
		puzzle_name = 'jan2710'
		puzzle_solver.fill( puzzle_name )
		diff = evaluate.compare_results( puzzle_name )
		evaluate.score_puzzle( diff )


if __name__ == '__main__':
	main()
