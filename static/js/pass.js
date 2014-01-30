//distributes each dancer to each of the choreographers within their desired range of dances
function init_distribute(all_dancers) {
	for (var d=0;d<all_dancers.length;d++) {
		var dancer = all_dancers[d];
		var pref = dancer.get_pref();
		var desired = dancer.get_desired();

		for (var i=0;i<desired;i++) {
			pref[i].add_to_current_hand(dancer);
		}
	}
}

function accept_dance(dancer_id, all_dancers, choreographer) {
	var dancer = find_dancer_by_id(all_dancers,dancer_id);

	dancer.accept(choreographer);
	choreographer.add_to_dance(dancer);
	choreographer.get_hand().splice(choreographer.get_hand().indexOf(dancer),1);
 	var num = choreographer.get_dance_list().length;

	var half_sel = document.getElementById('half_'+dancer_id);
	half_sel.remove();

	var mini_queue = document.getElementById('mini_'+dancer_id);
	mini_queue.remove();

	var a_table = document.getElementById('a_table');
	var new_row = a_table.insertRow(a_table.rows.length);

	var order_cell  = new_row.insertCell(0);
    order_cell.appendChild(document.createTextNode(num));
	var name_cell  = new_row.insertCell(1);
    name_cell.appendChild(document.createTextNode(dancer.get_name()));
}

function deny_dance(dancer_id, all_dancers) {
	var dancer = find_dancer_by_id(all_dancers,dancer_id);

	dancer.deny();

	var half_sel = document.getElementById('half_'+dancer_id);
	half_sel.remove();

	var mini_queue = document.getElementById('mini_'+dancer_id);
	mini_queue.remove();

}

function return_dance(dancer_id, choreographer) {
	var dancer = find_dancer_by_id(all_dancers,dancer_id);

	dancer.deny();
	dancer.maybe(choreographer);

	var half_sel = document.getElementById('half_'+dancer_id);
	half_sel.remove();

	var mini_queue = document.getElementById('mini_'+dancer_id);
	mini_queue.remove();

}

init_distribute(all_dancers);