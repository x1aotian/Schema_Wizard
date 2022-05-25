$(document).ready(function(){
    $("#source").change(function(){
        $(".src").addClass("hidden");
        $(".src").attr("required", true);
        $("#src-"+$(this).val()).removeClass("hidden");
        $("#src-"+$(this).val()).removeAttr('required');
    });
    $("#dest").change(function(){
        $(".dest").addClass("hidden");
        $(".dest").attr("required", true);
        $("#dest-"+$(this).val()).removeClass("hidden");
        $("#dest-"+$(this).val()).removeAttr('required');
    });
});