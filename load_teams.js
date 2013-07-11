$(document).ready(function(){
$.getJSON('/teams', function(data, textStatus, req) {
            $(data).each(function(i, v) {
                    var team = v["team_name"]
                    $('[name="team_name"]').append("<option value='"+team+"'>"+team+"</option>")
                })
            }).fail(function(req, textStatus, error) {
                console.log("Error: " + textStatus + " -- " + error)
        })
})
