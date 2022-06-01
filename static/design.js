// $(document).ready(function(){
//     $("#chooseType").change(function(){
//         $(".content").addClass("hidden");
//         $("#content-"+$(this).val()).removeClass("hidden");
//     });
// });
// var context = {
//     'type_list': ["Numbers", "Currency", "String", "Email", "Phone_Number", "URL", "Date", "Time", "DateTime"],
//     'type_list_demands': [["prec", "minv", "maxv"], ["curr_type", "prec", "minv", "maxv"], ["minl","maxl"], ["minl","maxl"], ["minl","maxl"], ["minl", "maxl"], ["max_year", "min_year"], [], ["max_year", "min_year"]]
// }

// var keyOptions = "<option value='default'>Select one below</option>";
            
// for (var i = 0; i < context['type_list'].length; i++) {
//     keyOptions += "<option value='" + context['type_list'][i] + "'>" + context['type_list'][i] + "</option>"
// }
// console.log(keyOptions)
// document.getElementById('chooseType').innerHTML = keyOptions;

// $(document).ready(function(){
//     $("#chooseType").change(function(){
//         $(".content").addClass("hidden");
//         $("#content-"+$(this).val()).removeClass("hidden");
//     });
// });
// var val = document.getElementById("type_list").value;
// const type_list = val.slice(1, -1).split(",");

// var keyOptions = "<option value='default'>Select one below</option>";
            
// for (var i = 0; i < type_list.length; i++) {
//     keyOptions += "<option value='" + i + "'>" + type_list[i].slice(1,-1) + "</option>"
// }
// document.getElementById('chooseType').innerHTML = keyOptions;

$(document).ready(function(){
    $("#chooseType").change(function(){
        $(".content").addClass("hidden");
        $("#content-"+$(this).val()).removeClass("hidden");
    });
});
var val = document.getElementById("type_list").value;
const type_list = val.slice(1, -1).split(", ");


var keyOptions = "<option value='default'>Select one below</option>";
            
for (var i = 0; i < type_list.length; i++) {
    console.log(type_list[i].slice(1,-1));
    keyOptions += "<option id ='" + i + "' value='" + type_list[i].slice(1,-1) + "'>" + type_list[i].slice(1,-1) + "</option>"
}
document.getElementById('chooseType').innerHTML = keyOptions;