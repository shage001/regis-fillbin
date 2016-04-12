'''
Temporary thing to split up puzzle testing
'''

import os
import sys
import puzzle_solver
import evaluate

def main():
	"""
	**********************************************************************************************************************
	Run on file execution
	"""
	# puzzle_name = WEEK[3]
	# puzzle_name = 'oct0515'
	# puzzle_name = 'dec3014'
	# puzzle_name = 'jan2710'

	## record puzzles done so far ##
	with open( 'done2.txt', 'r' ) as done_file:
		done = done_file.read().splitlines()
	done_file.close()


	for puzzle_name in os.listdir( 'puzzles2/' ):

		## avoid hidden files and previously solved ones ##
		if len( puzzle_name ) != 7 or puzzle_name in done:
			continue
		puzzle_solver.fill( puzzle_name )
		diff = evaluate.compare_results( puzzle_name )
		evaluate.score_puzzle( diff )
		with open( 'done2.txt', 'a' ) as done_file:
			done_file.write( puzzle_name + '\n' )
		done_file.close()



if __name__ == '__main__':
	main()
