function accept_dancer(obj) {
	var dancer_id = $(obj).parent().data("dancer-id");
	var dance_id = $(obj).parent().data("dance-id");
	already_seen.push(dancer_id)
	$(obj).parent().parent().remove();
	$.ajax({
		type: "POST",
		async: false,
		data: { dancer_id: dancer_id, dance_id: dance_id },
		url: "http://127.0.0.1:8000/auditions/S14/accept_dancer/",
		success: function(response){
			response = JSON.parse(response);
	        dancers = response.dancers
	        display_dancers(dancers);

	    }
	});
}
function reject_dancer(obj) {
	var dancer_id = $(obj).parent().data("dancer-id");
	var dance_id = $(obj).parent().data("dance-id");
	already_seen.push(dancer_id)
	$(obj).parent().parent().remove();
	$.ajax({
		type: "POST",
		async: false,
		data: { dancer_id: dancer_id, dance_id: dance_id },
		url: "http://127.0.0.1:8000/auditions/S14/reject_dancer/",
		success: function(response){
			response = JSON.parse(response);
	        dancers = response.dancers
	        display_dancers(dancers);

	    }
	});
}

function pull_prefs(already_seen) {
	prefs = []
	$.ajax({
		async: false,
		url: "http://127.0.0.1:8000/auditions/S14/selection_prefsheets/2",
		success: function(response){
			response = JSON.parse(response);
	        pulled_dancers = response.dancers;
	        display_dancers(pulled_dancers);
	        pulled_dancers.forEach(function(pulled_dancer) {
	        	already_seen.push(pulled_dancer.id);
	        });
	        pulled_prefs = response.prefs;
	        pulled_prefs.forEach(function(pulled_pref) {
	        	if (already_seen.indexOf(pulled_pref.user.dancer_id)===-1) {
	        		prefs.push(pulled_pref);
	        	}
	        });
	    }
	});
	return prefs;
}

function display_prefs(prefs) {
	$( "#center-column" ).empty();
	$.each(prefs, function(i, pref) {
		var source   = $("#profile-template").html();
		var template = Handlebars.compile(source);
		var name = pref.user.first_name+" "+pref.user.last_name;
		var conflicts = pref.prefsheet.conflicts;
		var id = pref.user.dancer_id;
		var context = {
			name: name,
			conflicts: conflicts,
			dance_id: pref.dance_id,
			dancer_id: pref.user.dancer_id,
			dances: pref.dances,
			desired: pref.prefsheet.desired_dances,
			accepted: pref.info.accepted_dances,
			rejected: pref.info.rejected_dances
		}
		var html = template(context);
		$( "#center-column" ).append(html);
	});
	$('#accept-button').click(function() {
		accept_dancer(this);
	});
	$('#reject-button').click(function() {
		reject_dancer(this);
	});
}

function display_dancers(dancers) {
	$('.dancers').empty();
	$.each(dancers, function(i, dancer) {
		$( ".dancers" ).append("<p>"+dancer.name+"</p>");
	});
}

var prefs = []
var dancer_queue = [];
var in_my_dance = [];
var already_seen = []
preferences = pull_prefs(already_seen);
display_prefs(preferences);


