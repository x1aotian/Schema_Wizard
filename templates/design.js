$(document).ready(function(){
    $("#chooseType").change(function(){
        $(".content").addClass("hidden");
        $("#content-"+$(this).val()).removeClass("hidden");
    });
});
var context = {
    'type_list': ["Numbers", "Currency", "String", "Email", "Phone_Number", "URL", "Date", "Time", "DateTime"],
    'type_list_demands': [["prec", "minv", "maxv"], ["curr_type", "prec", "minv", "maxv"], ["minl","maxl"], ["minl","maxl"], ["minl","maxl"], ["minl", "maxl"], ["max_year", "min_year"], [], ["max_year", "min_year"]]
}
/*
var fieldType = {"Number": ["prec", "minv", "maxv"],
                "Currency": ["curr_type", "prec", "minv", "maxv"],
                "String": ["minl","maxl"],
                "Email": ["minl","maxl"],
                "Phone_Number": ["minl","maxl"],
                "URL": ["minl","maxl"],
                "Date": ["max_year", "min_year"],
                "Time": [],
                "DateTime": ["max_year", "min_year"]
                };
*/

var keyOptions = "<option value='default'>Select one below</option>";
            
for (let type in context['type_list']) {
    keyOptions += "<option value='" + type + "'>" + type + "</option>"
}
console.log(keyOptions)
document.getElementById('chooseType').innerHTML = keyOptions;