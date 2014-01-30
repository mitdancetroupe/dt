//abstract Dancer datatype
function Dancer() {
	this.audition_id = 0;
	this.full_name = '';
	this.bio = '';
	this.pic = ''; //img src
	this.phone = '';
	this.conflicts = []; //recurring date/time
	this.desired = 0; //number of dances a dancer wants to be in; max 4
	this.pref = []; //dances preffed in order of preference, list of choreographer objects
	this.accepted = []; //dances that dancer has been accepted in max size 4
	this.state = 0; //indicates which preffed choreographer they are being evaluated by
	this.return_to = []; //holds all choreographers to "return to" in order of pref number, by pref number
	this.sad_face = false;
	this.kerberos = '';
	this.gmail = '';
};

//compiles dancer information
Dancer.prototype.compile = function(id, name, bio, pic, phone, conflicts, desired, pref, kerberos, gmail) {

	this.full_name = name;
	this.bio = bio;
	this.pic = pic;
	this.phone = phone;
	this.conflicts = conflicts;
	this.desired = desired;
	this.pref = pref;
	this.audition_id = id;
	this.kerberos = kerberos;
	this.gmail= gmail;
}

Dancer.prototype.get_pref = function() {
	return this.pref;
}

Dancer.prototype.get_state = function() {
	return this.state;
}

Dancer.prototype.get_name = function() {
	return this.full_name;
}


Dancer.prototype.get_desired = function() {
	return this.desired;
}

Dancer.prototype.get_id = function() {
	return this.audition_id;
}

Dancer.prototype.is_done = function() {
	if (this.state === 100) {
		return true;
	}
	return false;
}

Dancer.prototype.accept = function(dance_name) {
	if (this.accepted.length < this.desired) {
		this.accepted.push(dance_name);
		this.state += 1;
	}
	if (this.accepted.length === this.desired) {
		this.state = 100; //state 5 indicated completion
	}
}

Dancer.prototype.deny = function() {
	//update the state of this dancer if they have not reached their last preffed dance
	if (this.state < this.pref.length-1) {
		this.state += 1;
	}
	//if they have reached their last preffed dance
	else if (this.state === this.pref.length) {
		//send the dancer to their return to's if they have any
		if ( this.return_to.length > 0 ) {
			this.state = this.return_to[0];
		}
		//else mark this dancer as complete
		else {
			this.state === 100;
		}
	}
}

Dancer.prototype.maybe = function(choreographer) {
	var pref_num = this.pref.indexOf(choreographer);
	this.return_to[pref_num] = choreographer;
	console.log(this.return_to);
}

//give the dancer a sad face if they are done and not in any dances
Dancer.prototype.eval_sad_face = function() {
	if (dancer.is_done && this.accepted === 0) {
		this.sad_face = true;
	}
}

//renders entire profile
Dancer.prototype.render_full = function() {

}

//only renders name and audition id
Dancer.prototype.render_mini = function(choreographer) {
	var qt = document.getElementById('q_table');
    var pref_num = this.pref.indexOf(choreographer) + 1;
    var new_row = qt.insertRow(qt.rows.length);
    var row_id = 'mini_'+ this.audition_id;
    new_row.setAttribute('id', row_id);

    var id_cell  = new_row.insertCell(0);
    id_cell.appendChild(document.createTextNode(this.audition_id));

    var name_cell = new_row.insertCell(1);
    name_cell.appendChild(document.createTextNode(this.full_name));

    var pref_cell = new_row.insertCell(2);
    pref_cell.appendChild(document.createTextNode(pref_num));

    var desired_cell = new_row.insertCell(3);
    desired_cell.appendChild(document.createTextNode(this.desired));
}

//renders photo, name, audition number, desired number of dancers, what dances they have been accepted by, pref number
Dancer.prototype.render_half = function() {

    var half = document.createElement('div');
    half.className = 'dancer_half';
    half.setAttribute('id', 'half_'+this.audition_id);
    var aud_num = '<div class="aud_num">#'+this.audition_id+'</div>';
    var img = '<img class="prof_pic" src='+this.pic+'>';
    var basic_info = '<div class="half"><p class="basic_info"><b>'+this.full_name+'</b><br/><br/>'+
    											this.bio+'<br/><br/>' +
    											this.accepted.length+' of '+this.desired+' dances accepted</p></div>';

    var pref = '<table border="1" class="pref_order"><th><pre> # </pre></th><th><pre> Dance Name </pre></th>';
    for (var i=0;i<this.pref.length;i++) {
        var pref_num = i+1;
        pref += '<tr><td>'+ pref_num +'</td>';
        pref += '<td>'+this.pref[i].get_name()+'</td></tr>';
    }
    pref += '</table>';

    half.innerHTML = aud_num + img + basic_info+ pref;

    return half;
}

function find_dancer_by_id(all_dancers,id) {
	for (var i=0;i<all_dancers.length;i++) {
		if (all_dancers[i].get_id().toString() === id.toString()) {
			return all_dancers[i];
		}
	}
}
