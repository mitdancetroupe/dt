$(document).ready(function() {
    var schedule_json = {};

    getScheduleJson();

    $(".schedule-checkbox").change(function(e) {
        updateJson(this);
    });

    function getScheduleJson() {
        $(".schedule-checkbox").each(function() {
            updateJson(this);
        });
    }

    function updateJson(e) {
        var checked = e.checked;
        var value = e.value;
        var day = value.slice(0,1);
        var time = value.slice(1,5);
        schedule_json[value] = {
            day: day,
            time: time,
            availability: checked ? 1 : 0
        };
        $("#schedule_json").val(JSON.stringify(schedule_json));
    }
});