$( document ).ready(function(){})

function Choreographer() {
	this.dance_name = '';
	this.dancer_list = [];
	this.current_hand = [[],[],[],[],[],[],[],[]]; 
}

Choreographer.prototype.add_to_current_hand = function(dancer) {
	var d_pref = dancer.get_pref();
	var pref = d_pref.indexOf(this);

	this.current_hand[pref].push(dancer);
}

Choreographer.prototype.get_hand = function() {
	return this.current_hand;
}

Choreographer.prototype.set_name = function(name) {
	this.dance_name = name;
}

Choreographer.prototype.get_name = function() {
	return this.dance_name;
}

Choreographer.prototype.add_to_dance = function(dancer) {
	this.dancer_list.push(dancer);
	
}

Choreographer.prototype.get_dance_list = function() {
	return this.dancer_list;
}