//##########################################
// Some click Events
//##########################################
// naive and just for testing;-)
$(document).on( 'click', '.marker-button', function() {
	//console.log('test')
	let marker_id = '#' + $(this).attr('data-marker'); 
	console.log( marker_id );
	$(marker_id).toggle(400);

});


$(document).on( 'click', '#settings-toggler', function() {
	let panel_status = $('.settings-panel').attr('aria-expanded');
	if(panel_status == 'true'){
		$(this).removeClass('fa-plus-circle');
		$(this).addClass('fa-minus-circle');
	} else {
		$(this).removeClass('fa-minus-circle');
		$(this).addClass('fa-plus-circle');
	}
});