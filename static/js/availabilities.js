var availabilities = _availabilities;
var choreographer_conflicts = _choreographer_conflicts;
var times = _times;
var days = _days;
var all_conflicts = _conflicts;
var day_to_print = {
    'u': 'Sunday',
    'm': 'Monday',
    't': 'Tuesday',
    'w': 'Wednesday',
    'r': 'Thursday',
    'f': 'Friday',
    's': 'Saturday',
};

var calculateTimeStr = function(time) {
    var mhour = Math.floor(parseInt(time)/100);
    var min = time % 100 ? '30' : '00';
    var suffix = mhour < 12 ? ' am' : ' pm';
    var hour = mhour%12 ? mhour%12 : 12;
    return hour + ':' + min + suffix;
}

var timedict = {}
_.forEach(times, function(time) {
    _.forEach(days, function(day) {
        timedict[day+time] = {}
        timedict[day+time]['conflicts'] = 0
        timedict[day+time]['unavailable'] = []
        timedict[day+time]['cc'] = false;
    })
});

choreographer_conflicts.forEach(function(availability) {
    slug = availability.day + availability.hour
    timedict[slug]['cc'] = true;
    timedict[slug]['unavailable'].push(availability.name);
});

_.forEach(availabilities, function(availability) {
    slug = availability.day + availability.hour
    if (availability.unavailable) {
        timedict[slug]['conflicts'] += 1
        timedict[slug]['unavailable'].push(availability.name)
    }
});

var table = document.createElement('table');

var row = table.insertRow(0);
var col = row.insertCell(0);
col.innerHTML = '';
_.forEach(days, function(day, index) {
    col = row.insertCell(index+1);
    col.innerHTML = day_to_print[day];
    col.setAttribute("data-col", index+1);
});
_.forEach(times, function(time, timeIndex) {
    row = table.insertRow(timeIndex+1);
    col = row.insertCell(0);
    col.innerHTML = calculateTimeStr(time);
    col.className = time;
    _.forEach(days, function(day, dayIndex) {
        col = row.insertCell(dayIndex+1);
        col.setAttribute("data-col", dayIndex+1);
        if (Number(time) < 1700 && _.contains(['m', 't', 'w', 'r', 'f'], day)) {
            col.innerHTML = '-'
        } else {
            conflicts = timedict[day+time]['conflicts']
            var unavailable = timedict[day+time]['unavailable'];

            col.innerHTML = conflicts;
            if (conflicts === 0) {
                col.className = 'zero';
            } else if (conflicts === 1) {
                col.className = 'one';
            } else if (conflicts === 2) {
                col.className = 'two';
            } else if (conflicts === 3) {
                col.className = 'three';
            } else if (conflicts === 4) {
                col.className = 'four';
            } else if (conflicts === 5) {
                col.className = 'five';
            } else if (conflicts === 6) {
                col.className = 'six';
            } else if (conflicts === 7) {
                col.className = 'seven';
            } else if (conflicts === 8) {
                col.className = 'eight';
            }
            if (timedict[day+time]['cc']) {
                col.className = 'cc';
            }
            col.className += ' timeslot';
            col.setAttribute('data-slug', day+time);
            col.addEventListener("mouseover", function() {
                $('.'+time).addClass('bold');
                $('#notavailable').html(_(unavailable).join(', '));
            }, false);
            col.addEventListener("mouseout", function() {
                $('.'+time).removeClass('bold');
            }, false);
        }
    });
});

$('#availability-table').html(table);

$('td').hover(function(e) {
    $(this).css({
        'color': '#fff'
    });
    $(this).parent().children().css({
        "font-weight": "bold"
    }).addClass('highlight');
    var col = parseInt($(this).attr('data-col') || '0') + 1;
    $('td:nth-child(' + col + ')').css({
        "font-weight": "bold"
    }).addClass('highlight');
}, function(e) {
    $(this).css({
        'color': '#000'
    });
    $(this).parent().children().css({
        "font-weight": "normal"
    }).removeClass('highlight');
    var col = parseInt($(this).attr('data-col') || '0') + 1;
    $('td:nth-child(' + col + ')').css({
        "font-weight": "normal"
    }).removeClass('highlight');
});

// $('.timeslot').click(function(e) {
//     var ul = $('<ul></ul>');
//     var slug = $(this).attr('data-slug');
//     $('#reasons-time').html(day_to_print[slug.substring(0,1)] + ' ' + calculateTimeStr(slug.substring(1,5)));
//     var conflicts = timedict[slug]['unavailable'].forEach(function(dancer) {
//         var li = $('<li></li>').append('<b>' + dancer + ':</b> ' + all_conflicts[dancer]);
//         $(ul).append(li);
//     });

//     $("#reasons").html(ul);
// });

