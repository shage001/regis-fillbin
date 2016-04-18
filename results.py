'''
Sam Hage
Thesis
Look at results of testing
4/2016
'''

import os
import evaluate
import matplotlib.pyplot as plt

DAYS_LABEL = [ '', 'Mon.', 'Tue.', 'Wed.', 'Thu.', 'Fri.', 'Sat.', 'Sun.', '' ]
DAYS = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ]
LETTERS = [ -1, 94.94, 94.12, 94.55, 92.96, 94.91, 94.97, 93.76, -1 ]
WORDS = [ -1, 85.92, 84.22, 84.89, 81.68, 86.01, 86.43, 83.36, -1 ]
MIN_LETTERS = [ -1, 83.76, 75.26, 79.67, 76.47, 73.52, 77.48, 83.28, -1 ]
MIN_WORDS = [ -1, 61.53, 55.84, 61.84, 52.85, 59.15, 59.72, 65.67, -1 ]

def main():
	"""
	**********************************************************************************************************************
	Main function to run on program execution
	"""
	# score_all_puzzles()
	graph()


def graph():
	"""
	**********************************************************************************************************************

	"""
	x = [ 0, 1, 2, 3, 4, 5, 6, 7, 8 ]
	plt.xticks( x, DAYS_LABEL )
	plt.plot( x, LETTERS, 'ro', label='Letters' )
	plt.plot( x, WORDS, 'bo', label='Words' )
	plt.plot( x, MIN_LETTERS, 'r_', label='Min. Score' )
	plt.plot( x, MIN_WORDS, 'b_', label='Min. Score' )
	plt.plot( x, [ -1, 100, 100, 100, 100, 100, 100, 100, -1 ], 'r_' )
	plt.plot( x, [ -1, 100, 100, 100, 100, 100, 100, 100, -1 ], 'b_' )
	plt.legend(loc='lower right')
	plt.ylim( [ 0, 100 ] )
	plt.xlabel( 'Day' )
	plt.ylabel( 'Avg. Percent Correct' )
	plt.show()

def score_all_puzzles():
	"""
	**********************************************************************************************************************

	"""
	scores = [ [], [], [], [], [], [], [] ]
	avgs = [ [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ], [ 0, 0 ] ]
	num_puzzles = [ 0, 0, 0, 0, 0, 0, 0 ]
	max_scores = [ [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ], [ 0, '' ] ]
	min_scores = [ [ 100, '' ], [ 100, '' ], [ 100, '' ], [ 100, '' ], [ 100, '' ], [ 100, '' ], [ 100, '' ] ]

	for puzzle_name in os.listdir( 'puzzles/' ):

		## avoid hidden files ##
		if len( puzzle_name ) != 7:
			continue
		try:
			diff = evaluate.compare_results( puzzle_name )
			letters_correct, words_correct = evaluate.score_puzzle( diff )
			day = os.listdir( 'puzzles/' + puzzle_name )[0][1:-4]

			day_min = min_scores[ DAYS.index( day ) ][0]
			if words_correct < day_min:
				min_scores[ DAYS.index( day ) ][0] = words_correct
				min_scores[ DAYS.index( day ) ][1] = puzzle_name

			# day_max = max_scores[ DAYS.index( day ) ][0]
			# if letters_correct > day_max and letters_correct < 99:
			# 	max_scores[ DAYS.index( day ) ][0] = letters_correct
			# 	max_scores[ DAYS.index( day ) ][1] = puzzle_name

			scores[ DAYS.index( day ) ].append( [ round( letters_correct, 2 ), round( words_correct, 2 ) ] )
		except:
			print( 'puzzle not solved yet' )

	for score in min_scores:
		print( score[0] )

	with open( 'scores.txt', 'w' ) as scores_file:

		scores_file.write( '# LETT\tWORDS\n' )
		for i in range( len( scores ) ):
			scores_file.write( '# ' + DAYS[i] + '\n' )

			for puzzle in scores[i]:
				scores_file.write( str( puzzle[0] ) + '\t' + str( puzzle[1] ) + '\n' )
				avgs[i][0] += puzzle[0]
				avgs[i][1] += puzzle[1]
				num_puzzles[i] += 1

	scores_file.close()

	with open( 'scores-avg.txt', 'w' ) as avg_scores_file:
		for i in range( len( scores ) ):
			avg_scores_file.write( '# ' + DAYS[i] + '\n' )
			avg_scores_file.write( str( round( avgs[i][0] / num_puzzles[i], 2 ) ) + '\t' + str( round( avgs[i][1] / num_puzzles[i], 2 ) ) + '\n' )
	avg_scores_file.close()


if __name__ == '__main__':
	main()
