dataMaker("f3");

$(".prox-checkbox").change(function() {
    $("#prox-" + this.value).toggle();
    $("#prox-" + this.value + "_slider").toggle();
});
