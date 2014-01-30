function load_selection(all_dancers, choreographer) {
	var hand = choreographer.get_hand();

	for (var i=0;i<hand.length;i++) {
		if (hand[i].length>0) {
			var pref_section = document.createElement('div');
			var pref_div_id = 'pref_'+i;
			pref_section.setAttribute('id', pref_div_id);

			// var pref_head =document.createElement('div');
			// pref_head.setAttribute('class','pref_head');
			// var pnum = i+1;
			// pref_head.innerHTML = 'Pref <b>'+ pnum +'</b> Dancers';
			// pref_section.appendChild(pref_head);

			for (var j=0;j<hand[i].length;j++) {
				var dancer = hand[i][j];
				var dancer_element = dancer.render_half();

				var button_div = document.createElement('div');
				button_div.setAttribute('class','button_container');
				var yes_button = document.createElement('input');
				var no_button = document.createElement('input');
				var maybe_button = document.createElement('input');

				yes_button.setAttribute('type', 'button');
				no_button.setAttribute('type', 'button');
				maybe_button.setAttribute('type', 'button');

				yes_button.setAttribute('class', 'yes_button');
				no_button.setAttribute('class', 'no_button');
				maybe_button.setAttribute('class', 'maybe_button');

				yes_button.setAttribute('name', dancer.get_id());
				no_button.setAttribute('name', dancer.get_id());
				maybe_button.setAttribute('name', dancer.get_id());

				yes_button.setAttribute('value', 'Yes');
				no_button.setAttribute('value', 'No');
				maybe_button.setAttribute('value', 'Return if not placed');

				yes_button.addEventListener("click", function(event) {
					accept_dance(event.target.name,all_dancers,choreographer);
				});

				no_button.addEventListener("click", function(event) {
					deny_dance(event.target.name,all_dancers);
				});

				maybe_button.addEventListener("click", function(event) {
					return_dance(event.target.name,all_dancers);
				});

				button_div.appendChild(yes_button);
				button_div.appendChild(no_button);
				button_div.appendChild(maybe_button);

				dancer_element.appendChild(button_div);
				pref_section.appendChild(dancer_element);
			}

	    var selection = document.getElementById('selection');
	    selection.appendChild(pref_section);

		}
	}
}
load_selection(all_dancers, c_main);
