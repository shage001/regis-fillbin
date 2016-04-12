/**
 * Sam Hage
 * Thesis
 * Generate HTML elements to display solved puzzles
 * 11/2015
 */


main();


/**********************************************************************************************************************
 * Main function to be run on program execution. Gets the day of the week from the URL
 * and uses it to generate the correct puzzle
 */
function main()
{
	// var week = [ 'oct0906', 'dec2899', 'jun0497', 'nov0515', 'nov0615', 'apr2796', 'nov0815' ];
	var week = [ 'dec1613', 'jul2313', 'aug1011', 'dec2712', 'feb1210', 'nov0610', 'aug1714' ];
	// var perfectWeek = [ 'apr0813', 'dec1614', 'apr0214', 'apr0110', 'apr3010', 'apr0911', 'aug3010' ];
	var days = [ 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday' ];
	var url = window.location.href;
	var paramIndex = url.indexOf( '?day=' );
	if ( paramIndex === -1 ) {
		var puzzle_name = week[0];
	}
	else {
		var day = url.slice( paramIndex + 5 );
		var puzzle_name = ( days.indexOf( day ) < week.length ) ? week[ days.indexOf( day ) ] : week[0];
	}
	loadFile( puzzle_name, createPuzzle );
}

/**********************************************************************************************************************
 * Functions to run on AJAX success and failure
 */
function xhrSuccess() { this.callback.apply( this ); }

function xhrError () { console.error( this.statusText ); }


/**********************************************************************************************************************
 * Try to load the file provided
 *
 * @param: {string} sURL Path to the file
 * @param: {function} fCallback Callback function
 */
function loadFile ( puzzle_name, fCallback )
{
	/* create a request and set its callback */
	var sURL = 'puzzles/' + puzzle_name + '/' + puzzle_name + '-diff.txt';
	var request = new XMLHttpRequest();
	request.callback = fCallback;
	request.onload = xhrSuccess;
	request.onerror = xhrError;

	/* open the request and send */
	request.open( 'GET', sURL, true );
	request.send( null );
}


/**********************************************************************************************************************
 * Callback function for the AJAX request. Displays the puzzle on the page.
 */
function createPuzzle()
{
	var puzzleText = this.responseText;
	// console.log( puzzleText.length );
	var dimension = Math.sqrt( puzzleText.length );

	/* resize for sunday puzzle */
	if ( dimension === 21 ) {
		var puzzleBox = document.getElementsByClassName( 'puzzle' )[0];
		puzzleBox.className = 'puzzle-large';
	}

	var k = 0;
	for ( var i = 0; i < dimension; i++ )
	{
		for ( var j = 0; j < dimension; j++ )
		{
			var square = document.createElement( 'div' );
			square.className = 'square';
			var letter = this.responseText[k];
			if ( letter === '0' ) {
				square.className = 'square blank';
			}
			else if ( letter.charCodeAt( 0 ) > 96 ) {
				square.className = 'square incorrect';
			}
			square.innerHTML = letter.toUpperCase();

			document.body.appendChild( square );
			k++;
		}
		document.body.appendChild( document.createElement( 'br' ) );
	}
}
