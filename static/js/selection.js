var prefs = null;
var dancers = null;

$.ajax({
	async: false,
	url: "http://127.0.0.1:8000/auditions/S14/selection_prefsheets/2",
	success: function(response){
		response = JSON.parse(response);
        dancers = response.dancers;
        prefs = response.prefs;
        load_prefs();
    }
});
function load_prefs() {
	$.each(prefs, function(i, pref) {
		var source   = $("#profile-template").html();
		var template = Handlebars.compile(source);
		var name = pref.user.first_name+" "+pref.user.last_name;
		var conflicts = pref.prefsheet.conflicts;
		var context = {name: name, conflicts: conflicts}
		var html = template(context);
		$( "#center-column" ).append(html);
	});
}



/*
<tr>
					  <td>{{dance.pref}}</td>
					  <td>{{dance.name}}</td>
					</tr>
					*/
