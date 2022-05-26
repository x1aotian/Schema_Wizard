$(document).ready(function(){
    $("#chooseType").change(function(){
        $(".content").addClass("hidden");
        $("#content-"+$(this).val()).removeClass("hidden");
    });
});
var type_list = "{{type_list}}";

var keyOptions = "<option value='default'>Select one below</option>";
            
for (var i = 0; i < type_list.length; i++) {
    keyOptions += "<option value='" + i + "'>" + type_list[i] + "</option>"
}
document.getElementById('chooseType').innerHTML = keyOptions;