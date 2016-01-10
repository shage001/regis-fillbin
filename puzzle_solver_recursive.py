
import ast
import time
import clue_scraper
import puzzle_structure

def main():
	"""
	**********************************************************************************************************************
	Main code to run on program execution
	"""
	fill( 'oct0515' )


def fill( puzzle_name ):
	"""
	**********************************************************************************************************************

	"""
	# puzzle_structure.read_raw_puzzle( puzzle_name )
	puzzle = puzzle_structure.create_puzzle( puzzle_name, 'skeleton' )
	# clue_scraper.lookup_all_clues( puzzle_name )

	puzzle_structure.sort_answers( puzzle_name )
	f = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'r' )
	answers = f.read().splitlines()[3:]
	for i in range( len( answers ) ):
		answers[i] = answers[i].strip().split( '\t' )
		answers[i] = [ int( answers[i][0] ), int( answers[i][1] ), answers[i][2], ast.literal_eval( answers[i][3] ), ast.literal_eval( answers[i][4] ) ]

	recursive_solver( puzzle, answers, 0 )
	puzzle_structure.print_puzzle( puzzle )


def recursive_solver( puzzle, answers, answer_index ):
	"""
	**********************************************************************************************************************

	"""
	time.sleep( .25 )
	puzzle_structure.print_puzzle( puzzle )
	## exit condition ##
	if ( answer_index == len( answers ) ):
		return 1

	cur_info = answers[ answer_index ]
	candidates = cur_info[4]
	print( answer_index, candidates )

	for candidate in candidates:
		if ( is_valid( candidate, puzzle, cur_info[0], cur_info[1], cur_info[2] ) ):
			puzzle = fill_answer( candidate, puzzle, cur_info[0], cur_info[1], cur_info[2] )
			if recursive_solver( puzzle, answers, answer_index + 1 ):
				return 1
			puzzle = fill_answer( ' ' * len( candidate ), puzzle, cur_info[0], cur_info[1], cur_info[2] )



def is_valid( answer, puzzle, row, col, direction ):
	"""
	**********************************************************************************************************************

	"""
	for i in range( len( answer ) ):
		if puzzle[row][col] != answer[i] and puzzle[row][col] != ' ':
			return 0
		if direction == 'across':
			col += 1
		else:
			row += 1
	return 1


def fill_answer( answer, puzzle, row, col, direction ):
	"""
	**********************************************************************************************************************

	"""
	for i in range( len( answer ) ):
		puzzle[row][col] = answer[i]
		if direction == 'across':
			col += 1
		else:
			row += 1
	return puzzle


if __name__ == '__main__':
	main()
