'''
Sam Hage
Thesis
Look at results of testing
4/2016
'''

import os
import evaluate

DAYS = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]

def main():
	"""
	**********************************************************************************************************************
	Main function to run on program execution
	"""
	scores = [ [], [], [], [], [], [], [] ]
	max_scores = [ [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ] ]
	i = 0
	for puzzle_name in os.listdir( 'puzzles/' ):
		i += 1

		## avoid hidden files ##
		if len( puzzle_name ) != 7:
			continue
		try:
			diff = evaluate.compare_results( puzzle_name )
			letters_correct, words_correct = evaluate.score_puzzle( diff )
			day = os.listdir( 'puzzles/' + puzzle_name )[0][1:-4]

			day_max = max_scores[ DAYS.index( day ) ][0]
			if letters_correct > day_max and letters_correct < 99:
				max_scores[ DAYS.index( day ) ][0] = letters_correct
				max_scores[ DAYS.index( day ) ][1] = puzzle_name

			scores[ DAYS.index( day ) ].append( [ round( letters_correct, 2 ), round( words_correct, 2 ) ] )
			# print( day )
		except:
			print( 'puzzle not solved yet' )
		# if i == 100:
		# 	break
	print( max_scores )

if __name__ == '__main__':
	main()
