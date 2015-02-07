$(document).ready(function() {
    var schedule_json = {};

    setupScheduleJson();

    $(".schedule-checkbox").change(function(e) {
        updateJson(this);
    });

    function setupScheduleJson() {
        var availabilityString = $("#id_availability").val();
        // initialize if not there yet
        if (!availabilityString) {
            $(".schedule-checkbox").each(function() {
                updateJson(this);
            });
        // otherwise populate
        } else {
            var availabilityJson = JSON.parse(availabilityString);
            $.each(availabilityJson, function(index, value) {
                var key = value.day + value.time;
                schedule_json[key] = value;
                var available = value.availability;
                $("#" + key)[0].checked = available ? false : true;
            });
        }
    }

    function updateJson(e) {
        var checked = e.checked;
        var value = e.value;
        var day = value.slice(0,1);
        var time = value.slice(1,5);
        schedule_json[value] = {
            day: day,
            time: time,
            availability: checked ? 0 : 1
        };
        var schedule_values = [];
        $.each(schedule_json, function(k, v) {
            schedule_values.push(v);
        });
        $("#id_availability").val(JSON.stringify(schedule_values));
    }
});