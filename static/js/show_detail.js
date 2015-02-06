$(document).ready(function() {
    $(".dance-div").on("click", function() {
        var danceId = $(this).context.id.slice(6);
        $("#modal-" + danceId).modal();
    });

    $("#contemporary").on("click", function() {
        $(".dance").hide();
        $(".contemporary").show();
    });

    $("#hip-hop").on("click", function() {
        $(".dance").hide();
        $(".hip-hop").show();
    });

    $("#all").on("click", function() {
        $(".dance").show();
    });
});