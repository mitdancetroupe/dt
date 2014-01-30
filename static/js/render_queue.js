function load_queue(all_dancers, choreographer) {
    for (var d=0;d<all_dancers.length;d++) {
        var dancer=all_dancers[d];
        //only load dancers that preffed this choreographer
        if ($.inArray(choreographer, dancer.get_pref()) > -1) {
            //don't render dancers that have been accepted or rejected from the dance
            if ($.inArray(dancer, choreographer.get_dance_list()) < 0) {
                dancer.render_mini(choreographer);
            }
        }
    }
}

load_queue(all_dancers, c_main);