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