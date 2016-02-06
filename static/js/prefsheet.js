$(document).ready(function() {

    $('.schedule-box').click(function(e) {
        var value = $(this).attr('data-slug');
        var available = parseInt($(this).attr('data-available'));
        if (parseInt(available)) {
            $(this).removeClass('green').addClass('red');
        } else {
            $(this).removeClass('red').addClass('green');
        }
        var newAvailability = available ? 0 : 1;
        $(this).attr('data-available', newAvailability);
        updateJson(newAvailability, value);
    });

    var schedule_json = {};

    setupScheduleJson();

    function setupScheduleJson() {
        var availabilityString = $("#id_availability").val();
        // initialize if not there yet
        if (!availabilityString) {
            $(".schedule-box").each(function() {
                var available = $(this).attr('data-available');
                var value = $(this).attr('data-slug');
                updateJson(available, value);
            });
        // otherwise populate
        } else {
            var availabilityJson = JSON.parse(availabilityString);
            $.each(availabilityJson, function(index, value) {
                var key = value.day + value.time;
                schedule_json[key] = value;
                var available = parseInt(value.availability);
                $("#" + key).attr('data-available', available ? 1 : 0);
                if (!available) {
                    $("#" + key).removeClass('green').addClass('red');
                }
            });
        }
    }

    function updateJson(available, value) {
        var day = value.slice(0,1);
        var time = value.slice(1,5);
        schedule_json[value] = {
            day: day,
            time: time,
            availability: available ? 1 : 0
        };
        var schedule_values = [];
        $.each(schedule_json, function(k, v) {
            schedule_values.push(v);
        });
        $("#id_availability").val(JSON.stringify(schedule_values));
    }
});