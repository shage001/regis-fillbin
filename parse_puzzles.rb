# Sam Hage
# Thesis
# 12/2015
# A .puz parser. Uses Sam Mullen's API https://github.com/samullen/acrosslite

DAYS = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
MONTHS = [ "", "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec" ]
PUZZLE_PATH = "../assets/dan/"
DEST_PATH = "puzzles/"

require 'acrosslite'

# for i in 0..100
puzzle_name = "nyt141230"
ac = Acrosslite.new( :filepath => PUZZLE_PATH + puzzle_name + ".puz" )


## parse the puzzle's date into my format ##
puzzle_date = MONTHS[ puzzle_name[5...7].to_i ] +
					  puzzle_name[7..-1] +
					  puzzle_name[3...5]


## find day of the week by scanning the puzzle file ##
file = File.open( "../assets/dan/nyt141230.puz", "r+" )
raw_content = file.read
to_start = raw_content.index( "NY Times" )
day_indices = []

DAYS.each {
	|day|
	index = raw_content.index( day, to_start )
	index = !index ? 10000 : index
	day_indices << index
}

weekday = DAYS[ day_indices.index( day_indices.min ) ].downcase


## create the header file ##
if !File.directory?( DEST_PATH + puzzle_date )
	Dir.mkdir( DEST_PATH + puzzle_date )
end
header_file = File.open( DEST_PATH + puzzle_date + "/." + weekday + ".txt", "w" )


## create the clues file for the puzzle ##
acrosses = ac.across
downs = ac.down
clue_file = File.open( DEST_PATH + puzzle_date + "/" + puzzle_date + "-clues.txt", "w" )
clue_file.write( "##" + weekday.upcase + " " + puzzle_date + "##\n" )
clue_file.write( "#ACROSS\n" )
acrosses.each {
	|across|
	clue_file.write( across.row.to_s + "\t" + across.column.to_s + "\t" + across.length.to_s + "\t" + across.clue.downcase + "\n" )
}
clue_file.write( "#DOWN\n" )
downs.each {
	|down|
	clue_file.write( down.row.to_s + "\t" + down.column.to_s + "\t" + down.length.to_s + "\t" + down.clue.downcase + "\n" )
}


## create skeleton file ##
skeleton_file = File.open( DEST_PATH + puzzle_date + "/" + puzzle_date + "-skeleton.txt", "w" )

skeleton = ac.diagram
skeleton.each {
	|row|
	row.each {
		|cell|
		if cell == "."
			cell = "0"
		end
		if cell == "-"
			cell = "_"
		end
		skeleton_file.write( cell + " " )
	}
	skeleton_file.write( "\n" )
}


## create skeleton file ##
solution_file = File.open( DEST_PATH + puzzle_date + "/" + puzzle_date + "-solution.txt", "w" )

solution = ac.solution
solution.each {
	|row|
	row.each {
		|cell|
		if cell == "."
			cell = "0"
		end
		solution_file.write( cell + " " )
	}
	solution_file.write( "\n" )
}
