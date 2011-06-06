(function($) {
    var addPref = function(prefTable) {
        totalForms = $("#id_prefs-TOTAL_FORMS", prefTable).val();
        $("#id_prefs-TOTAL_FORMS", prefTable).val(totalForms++);
    }; 
})(jQuery);
