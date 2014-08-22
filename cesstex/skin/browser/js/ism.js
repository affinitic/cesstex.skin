/*recherche sur la table experience*/
$(document).ready(function(){

  $(function() {
    $("#nom_eleve").autocomplete({
        source: function(request, response) {
            $.ajax({
                url: "eleve-searchJSON",
                dataType: "json",
                data: {
                    featureClass: "P",
                    style: "full",
                    maxRows: 12,
                    name_startsWith: request.term
                },
                success: function(data) {
                    response($.map(data, function(item) {
                        return {
                            label: item,
                            value: item
                        }
                    }));
                }
            });
        },
        minLength: 2,
        open: function() {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function() {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });
});
});


$(document).ready(function() {
    $("#declencheur").click(function () {
    $(".evenement-historique").toggle("slow");
    });
});