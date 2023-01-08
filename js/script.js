$(document).ready(function() {
    var visibleRows = 0;

    if ($(".row").length < 5) {
        $(".loadMoreBttn").hide();
    }
    
    $(window).on("load", function() {
        $(".row.displayNone").each(function(i) {
            if (i < 5) {
                $(this).removeClass("displayNone");
                visibleRows++;
            }
        })
    })
    
    $(".loadMoreBttn").on("click", function() {
        $(".row.displayNone").each(function(i) {
            if (i < 5) {
                $(this).removeClass("displayNone");
                visibleRows++;
            }
            
            if (visibleRows == $(".row:not(.displayNone)").length) {
                $(".loadMoreBttn").hide();
            }
        })
    })
})