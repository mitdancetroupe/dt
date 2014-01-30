var all_dancers = [];

var c_main = new Choreographer();
c_main.set_name('Casey');
var c2 = new Choreographer();
c2.set_name('Bex');
var c3 = new Choreographer();
c3.set_name('Kristin');
var c4 = new Choreographer();
c4.set_name('Danyi');
var c5 = new Choreographer();
c5.set_name('Mason');

var all_c = [];
all_c.push(c_main); all_c.push(c2); all_c.push(c3); all_c.push(c4); all_c.push(c5);

var filler = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse congue lacus sed augue euismod, quis cursus nisl congue. Donec risus urna, facilisis et urna ac, malesuada mattis lacus. Nunc vehicula blandit euismod. ';

var d1 = new Dancer();
d1.compile('Kristin Au', filler , 'xxxxxxx', 'img/kristin.jpg', [], 4, [c_main,c2,c3,c4,c5], 1);

var d2 = new Dancer();
d2.compile('Rebecca Lin', filler , 'xxxxxxx', 'img/bex.jpg', [], 4, [c_main,c2,c3,c4,c5], 2);

var d3 = new Dancer();
d3.compile('Ami Wang', filler , 'xxxxxxx', 'img/ami.jpg', [], 3, [c2,c_main,c3,c4,c5], 3);


all_dancers.push(d1);
all_dancers.push(d2);
all_dancers.push(d3);
