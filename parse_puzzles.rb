require 'acrosslite'


# for i in 0..100
ac = Acrosslite.new( :filepath => "../assets/dan/nyt141230.puz" )

## find day of the week by scanning the puzzle file ##
file = File.open( "../assets/dan/nyt141230.puz", "r+" )
raw_content = file.read
to_start = raw_content.index( "NY Times" )
days = [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ]
day_indices = []

days.each {
	|day|
	index = raw_content.index( day, to_start )
	index = !index ? 10000 : index
	day_indices << index
}

weekday = days[ day_indices.index( day_indices.min ) ].downcase
puts weekday



acrosses = ac.across
downs = ac.down

# puts acrosses[0].row.to_s + "\t" + acrosses[0].column.to_s + "\t" + acrosses[0].length.to_s + "\t" + acrosses[0].clue
