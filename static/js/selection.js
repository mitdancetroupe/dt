function accept_dancer(obj) {
	var dancer_id = $(obj).parent().data("dancer-id");
	var dance_id = $(obj).parent().data("dance-id");
	var slug = $('#show_info').data("slug");
	$(obj).parent().parent().remove();
	$.ajax({
		type: "POST",
		data: { dancer_id: dancer_id, dance_id: dance_id },
		url: "http://127.0.0.1/auditions/"+slug+"/accept_dancer/",
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
	var slug = $('#show_info').data("slug");
	$(obj).parent().parent().remove();
	$.ajax({
		type: "POST",
		data: { dancer_id: dancer_id, dance_id: dance_id },
		url: "http://127.0.0.1/auditions/"+slug+"/reject_dancer/",
		success: function(response){
			response = JSON.parse(response);
	        dancers = response.dancers
	        display_dancers(dancers);

	    }
	});
}
function return_dancer(obj) {
	var dancer_id = $(obj).parent().data("dancer-id");
	var dance_id = $(obj).parent().data("dance-id");
	var slug = $('#show_info').data("slug");
	$(obj).parent().parent().remove();
	$.ajax({
		type: "POST",
		data: { dancer_id: dancer_id, dance_id: dance_id },
		url: "http://127.0.0.1/auditions/"+slug+"/return_dancer/",
		success: function(response){
			response = JSON.parse(response);
	        dancers = response.dancers
	        display_dancers(dancers);

	    }
	});
}

function pull_prefs() {
	prefs = []
	var slug = $('#show_info').data("slug");
	var dance_id = $('#show_info').data("id");
	$.ajax({
		async: false,
		url: "http://127.0.0.1/auditions/"+slug+"/selection_prefsheets/"+dance_id,
		success: function(response){
			response = JSON.parse(response);
	        pulled_dancers = response.dancers;
	        display_dancers(pulled_dancers);
	        pulled_prefs = response.prefs;
	        pulled_prefs.forEach(function(pulled_pref) {
        		prefs.push(pulled_pref);
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
			photo: pref.user.photo,
			name: name,
			conflicts: conflicts,
			experience: pref.user.experience,
			dance_id: pref.dance_id,
			dancer_id: pref.user.dancer_id,
			dances: pref.dances,
			desired: pref.prefsheet.desired_dances,
			accepted: pref.info.accepted_dances,
			rejected: pref.info.rejected_dances,
			prefed: pref.prefsheet.prefed,
		}
		var html = template(context);
		$( "#center-column" ).append(html);
	});
	$('.accept-button').click(function() {
		accept_dancer(this);
	});
	$('.reject-button').click(function() {
		reject_dancer(this);
	});
	$('.return-button').click(function() {
		return_dancer(this);
	});
}

function display_dancers(dancers) {
	$('.dancers').empty();
	$.each(dancers, function(i, dancer) {
		$( ".dancers" ).append("<tr><td>"+dancer.name+"</td><td>"+dancer.conflicts+"</td></tr>");
	});
}

var prefs = []
var dancer_queue = [];
var in_my_dance = [];
preferences = pull_prefs();
display_prefs(preferences);
setInterval(
	function(){
		preferences = pull_prefs();
		display_prefs(preferences);
	},3000);

