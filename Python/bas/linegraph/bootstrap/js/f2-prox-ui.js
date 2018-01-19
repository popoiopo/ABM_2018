dataMaker("f2");

$(".prox-checkbox").change(function() {
    $("#prox-" + this.value).toggle();
    $("#prox-" + this.value + "_slider").toggle();
});
