import ast
import sys
import time
import clue_scraper
import puzzle_structure

TIME_DELAY = .1
WORDS_FILE = 'assets/words-answers.txt'
WIKI_PATH_3 = 'assets/wiki-3.txt'
WIKI_PATH_4 = 'assets/wiki-4.txt'
WIKI_PATH_5 = 'assets/wiki-5.txt'
WIKI_PATH_6 = 'assets/wiki-6.txt'
WIKI_PATH_7 = 'assets/wiki-7+.txt'

def fill( puzzle_name ):
	"""
	**********************************************************************************************************************
	This does all the work solving the puzzle, starting with reading the raw
	input, then generating all candidate answers and filling the grid

	@param: {string} puzzle_name
	"""
	## read the raw puzzle input ##
	puzzle_structure.read_raw_puzzle( puzzle_name )
	## create a blank skeleton ##
	puzzle = puzzle_structure.create_puzzle( puzzle_name, 'skeleton' )
	## scrape all the clues ##
	clue_scraper.lookup_all_clues( puzzle_name )

	## ask for input to keep solving ##
	# print( 'Answers computed. Proceed with solving? ' )
	# cont = sys.stdin.readline()

	## keep track of the puzzle at the previous iteration to control ##
	## how long to solve at each step ##
	previous_puzzle_state = []

	puzzle_structure.sort_answers( puzzle_name )
	f = open( 'puzzles/' + puzzle_name + '/' + puzzle_name + '-answers.txt', 'r' )
	answers = f.read().splitlines()[3:]

	## extract answer data into list ##
	for i in range( len( answers ) ):
		answers[i] = answers[i].strip().split( '\t' )
		answers[i][0] = int( answers[i][0] )
		answers[i][1] = int( answers[i][1] )
		answers[i][3] = ast.literal_eval( answers[i][3] )
		answers[i][4] = ast.literal_eval( answers[i][4] )

	## fill singleton answers and update the candidates until this no longer ##
	## yields any change in the puzzle ##
	while puzzle != previous_puzzle_state:
		## update previous state ##
		previous_puzzle_state = [ row[:] for row in puzzle ]
		## fill all singletons, update possibilites, and resort ##
		answers, puzzle = fill_all_singletons( answers, puzzle, True )
		answers = update_candidates( answers, puzzle )
		answers = sorted( answers, cmp=puzzle_structure.compare_answers )
		answers = refactor_answers( answers )


	previous_puzzle_state = []
	## update answers with single word and wikipedia title searches ##
	## then fill singletons until this no longer yields any change ##
	while puzzle != previous_puzzle_state:
		## update previous state ##
		previous_puzzle_state = [ row[:] for row in puzzle ]
		answers = search_dictionaries( answers )
		answers = sorted( answers, cmp=puzzle_structure.compare_answers )
		answers = refactor_answers( answers )
		## fill the singletons ##
		answers, puzzle = fill_all_singletons( answers, puzzle, False )
		answers = update_candidates( answers, puzzle )


	## fill based on the first candidate. this is pretty arbitrary ##
	for answer in answers:
		if len( answer[4] ) > 0:
			puzzle = fill_answer( answer[4][0], puzzle, answer[0], answer[1], answer[2] )
		## clear console using escape sequence ##
		print( chr( 27 ) + '[2J' )
		## print the puzzle to stdout ##
		puzzle_structure.print_puzzle( puzzle )
		time.sleep( TIME_DELAY )

	## fill the rest of the squares with 'E'. this is extremely arbitrary ##
	puzzle = fill_empty_squares( puzzle )

	## write the final output for evaluation ##
	puzzle_structure.write_puzzle( puzzle_name, puzzle )


def fill_all_singletons( answers, puzzle, ignore_longs ):
	"""
	**********************************************************************************************************************
	Fills the grid with all singleton answers, i.e. answers that are the only
	candidate. Remove filled answers once filled

	@param: {string[][]} answers The list of information about each clue
	@param: {string[][]} puzzle The current grid representation
	@param: {boolean} ignore_longs When true, ignore long answers, as they are
								   more likely to have generated a false positive
	@return: {string[][], string[][]} The updated answers and puzzle state
	"""
	to_remove = []
	for info in answers:

		## clear console using escape sequence ##
		print( chr( 27 ) + '[2J' )
		## print the puzzle to stdout ##
		puzzle_structure.print_puzzle( puzzle )
		time.sleep( TIME_DELAY )

		candidates = info[4]
		if len( candidates ) != 1:
			break
		answer = candidates[0]
		## ignore long answers ##
		if len( answer ) > 6 and ignore_longs:
			continue
		row = info[0]
		col = info[1]
		direction = info[2]
		## fill the answer ##
		fill_answer( answer, puzzle, row, col, direction )
		to_remove.append( info )

	## remove all filled answers ##
	for info in to_remove:
		answers.remove( info )

	return answers, puzzle


def update_candidates( answers, puzzle ):
	"""
	**********************************************************************************************************************
	Update the candidate answer lists for all clues based on patterns on the
	board. Also update the pattern for empty candidate lists so they can be
	searched in dictionaries later.

	@param: {string[][]} answers The list of information about each clue
	@param: {string[][]} puzzle The current grid representation
	@return: {string[][]} Updated answers
	"""
	for i in range( len( answers ) ):
		## get the current pattern in the grid ##
		row = answers[i][0]
		col = answers[i][1]
		direction = answers[i][2]
		pattern = ''
		for j in range( len( answers[i][3][1] ) ):
			pattern += puzzle[row][col]
			if direction == 'across':
				col += 1
			else:
				row += 1

		## check all candidates and remove conflicting ones ##
		updated_candidates = []
		for candidate in answers[i][4]:
			include = True
			for k in range( len( candidate ) ):
				if candidate[k] != pattern[k] and pattern[k] != ' ':
					include = False
					break
			if include:
				updated_candidates.append( candidate )

		answers[i][4] = updated_candidates

		## update the pattern ##
		answers[i][3][1] = pattern.replace( ' ', '?' )

	return answers


def search_dictionaries( answers ):
	"""
	**********************************************************************************************************************
	Search clues in word lists and wikipedia list

	@param: {string[][]} answers The list of information about each clue
	@return: {string[][]} Updated answers
	"""
	words = clue_scraper.load_clues( WORDS_FILE )
	wiki_3 = clue_scraper.load_clues( WIKI_PATH_3 )
	wiki_4 = clue_scraper.load_clues( WIKI_PATH_4 )
	wiki_5 = clue_scraper.load_clues( WIKI_PATH_5 )
	wiki_6 = clue_scraper.load_clues( WIKI_PATH_6 )
	# wiki_7 = clue_scraper.load_clues( WIKI_PATH_7 )
	wiki_titles = [ wiki_3, wiki_4, wiki_5, wiki_6 ]

	message = 'Searching dictionaries'
	j = 0
	for i in range( len( answers ) ):
		sys.stdout.write( '\r                                ' )
		sys.stdout.write( '\r' + message + ( j % 4 )*'.' + ( 5 - j % 4 )*' ' )
		sys.stdout.flush()
		j += 1
		pattern = answers[i][3][1]
		if len( answers[i][4] ) == 0:
			answers[i][4] = clue_scraper.single_word_match( pattern, words )
			# print( answers[i][4] )
			if len( answers[i][4] ) == 0 and len( pattern ) < 7:
				# length = len( pattern )
				# if length > 7:
				# 	length = 7
				answers[i][4] = clue_scraper.wiki_title_match( pattern, wiki_titles[ len( pattern ) - 3 ] )

	print( 'Done.' )
	answers = sorted( answers, cmp=puzzle_structure.compare_answers )
	num_answers = len( answers )

	for i in range( num_answers ):
		## find first non-empty answer list ##
		if len( answers[i][4] ) != 0:
			break

	## move all empties to the back ##
	answers = answers[i:] + answers[:i]
	return answers


def refactor_answers( answers ):
	"""
	**********************************************************************************************************************
	Move the clues with empty candidate lists to the end since after the sort
	they will be at the top.

	@param: {string[][]} answers The list of information about each clue
	@return: {string[][]} Updated answers
	"""
	num_answers = len( answers )

	for i in range( num_answers ):
		## find first non-empty answer list ##
		if len( answers[i][4] ) != 0:
			break

	## move all empties to the back ##
	answers = answers[i:] + answers[:i]
	return answers


def fill_empty_squares( puzzle ):
	"""
	**********************************************************************************************************************
	Fill any remaining squares with 'E' since it's the most common letter

	@param: {string[][]} puzzle The current puzzle
	@param: {string[][]} The updated puzzle
	"""
	height = len( puzzle )
	width = len( puzzle[0] )

	## find empty squares ##
	for i in range ( height ):
		for j in range ( width ):
			if puzzle[i][j] == ' ':
				puzzle[i][j] = 'E'
				## clear console using escape sequence ##
				print( chr( 27 ) + '[2J' )
				## print the puzzle to stdout ##
				puzzle_structure.print_puzzle( puzzle )
				time.sleep( TIME_DELAY )

	return puzzle


def fill_answer( answer, puzzle, row, col, direction ):
	"""
	**********************************************************************************************************************
	Fill a single answer in the puzzle

	@param: {string[][]} answers The list of information about each clue
	@param: {string[][]} puzzle The current grid representation
	@param: {int} row The answer row
	@param: {int} col The answer column
	@param: {string} direction The direction of the clue
	@return: {string[][]} The updated puzzle
	"""
	for i in range( len( answer ) ):
		if puzzle[row][col] == ' ':
			puzzle[row][col] = answer[i]
		if direction == 'across':
			col += 1
		else:
			row += 1
	return puzzle
