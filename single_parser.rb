#!/usr/bin/env ruby
# Sam Hage
# Thesis
# 4/2016
# A lighter .puz parser for one puzzle. Uses Sam Mullen's API https://github.com/samullen/acrosslite

require 'acrosslite'

DAYS = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
DAYS_SHORT = [ "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun" ]
PUZZLE_PATH = "/Users/samhage/Downloads/"
DEST_PATH = "puzzles/"

# See String#encode
encoding_options = {
	:invalid           => :replace,  # Replace invalid byte sequences
	:undef             => :replace,  # Replace anything not defined in ASCII
	:replace           => '',        # Use a blank for those replacements
	:universal_newline => true       # Always break lines with \n
}

## get downloaded files in order of date modified ##
filenames = []

Dir.foreach( PUZZLE_PATH ) do
	|file|
	filenames << ( PUZZLE_PATH + file )
end

filenames = filenames.sort_by { |filename| File.mtime( filename ) }.reverse
puzzle_name = ""
filenames.each { # find most recent puzzle
	|f|
	if File.basename( f ).length == 11 && File.basename( f ).include?( ".puz" )
		puzzle_name = File.basename( f )
		break
	end
}

ac = Acrosslite.new( :filepath => PUZZLE_PATH + puzzle_name )

## get puzzle name/date in my format, then write to log file ##
puzzle_date = File.basename( puzzle_name, ".puz" ).downcase
log_file = File.open( "log.txt", "w" )
log_file.write( puzzle_date )
log_file.close

## find day of the week by scanning the puzzle file ##
file = File.open( PUZZLE_PATH + puzzle_name, "r+" )
raw_content = file.read
file.close
to_start = raw_content.index( "NY Times" )

if !to_start # check other format
	to_start = raw_content.index( "New York Times" )
end

if !to_start # neither of above
	to_start = 0
end

day_indices = []

DAYS.each {
	|day|
	index = raw_content.index( day, to_start )
	index = !index ? 10000 : index
	day_indices << index
}

if day_indices.min == 10000
	day_indices = []
	DAYS_SHORT.each {
		|day|
		index = raw_content.index( day, to_start )
		index = !index ? 10000 : index
		day_indices << index
	}
end

weekday = DAYS[ day_indices.index( day_indices.min ) ].downcase


## create the header file ##
if !File.directory?( DEST_PATH + puzzle_date )
	Dir.mkdir( DEST_PATH + puzzle_date )
end
header_file = File.open( DEST_PATH + puzzle_date + "/." + weekday + ".txt", "w" )
header_file.close


## create the clues file for the puzzle ##
acrosses = ac.across
downs = ac.down
clue_file = File.open( DEST_PATH + puzzle_date + "/" + puzzle_date + "-clues.txt", "w" )
clue_file.write( "## " + weekday.upcase + " " + puzzle_date + " ##\n" )
clue_file.write( "# ACROSS\n" )
acrosses.each {
	|across|
	cur_clue = across.clue.encode( Encoding.find( "ASCII" ), encoding_options ) # handle unicode chars
	clue_file.write( across.row.to_s + "\t" + across.column.to_s + "\t" + across.length.to_s + "\t" + cur_clue.downcase + "\n" )
}
clue_file.write( "# DOWN\n" )
downs.each {
	|down|
	cur_clue = down.clue.encode( Encoding.find( "ASCII" ), encoding_options ) # handle unicode chars
	# puts down.clue
	clue_file.write( down.row.to_s + "\t" + down.column.to_s + "\t" + down.length.to_s + "\t" + cur_clue.downcase + "\n" )
}

clue_file.close


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

skeleton_file.close


## create solution file ##
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

solution_file.close
