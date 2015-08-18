'use strict';

// On Ready

$(function() {

	 $('#myform').on('submit', function(e){
			e.preventDefault();
			console.log("test");

			var $form = $( this ),
			name = $form.find( "input[name='UserName']" ).val(),
			expr = $form.find( "input[name='InputDateTime']" ).val(),
			url = $form.attr( "action" );

			// Send the data using post
			var posting = $.post( url, { UserName:name, InputDateTime:expr } );

			// Put the results in a div
			posting.done(function( data ) {
				$( "#my_url" ).replaceWith(' <a href="' + data + '" target="_blank">' + data + '</a>');
			});

		});

});