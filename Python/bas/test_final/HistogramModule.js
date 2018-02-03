var HistogramModule = function(bins, canvas_width, canvas_height) {

    // Create the tag:
    var canvas_tag = "<canvas id='histo_canvas' width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "></canvas>";
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("#elements1").append(canvas);
    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");

    // Prep the chart properties and series:
    var datasets = [{
        label: "# of beers",
        backgroundColor: ['rgba(215,48,39,0.2)',
                          'rgba(244,109,67,0.2)',
                          'rgba(253,174,97,0.2)',
                          'rgba(254,224,144,0.2)',
                          'rgba(255,255,191,0.2)',
                          'rgba(224,243,248,0.2)',
                          'rgba(171,217,233,0.2)',
                          'rgba(116,173,209,0.2)',
                          'rgba(69,117,180,0.2)'],
            borderColor: ['rgba(215,48,39,0.6)',
                          'rgba(244,109,67,0.6)',
                          'rgba(253,174,97,0.6)',
                          'rgba(254,224,144,0.6)',
                          'rgba(255,255,191,0.6)',
                          'rgba(224,243,248,0.6)',
                          'rgba(171,217,233,0.6)',
                          'rgba(116,173,209,0.6)',
                          'rgba(69,117,180,0.6)'],
            data: []
    }];

    // Add a zero value for each bin
    for (var i in bins)
        datasets[0].data.push(0);

    var data = {
        labels: bins,
        datasets: datasets
    };

    var options = {
        scaleBeginsAtZero: true,
        responsive: false,
        title: {
          display: true,
          text: "# of beers drank per person"
        },
        legend: {
          display:false
        }
    };

    console.log(data);

    // Create the chart object
    // var chart = new Chart(context).Bar(data, options);
    var chart = new Chart(context, {
        type: 'bar',
        data: data,
        options: options
    });
    console.log(chart.data.datasets[0]);

    this.render = function(data) {
        for (var i in data)
            chart.data.datasets[0].data[i] = data[i];
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        chart = new Chart(context, {
        type: 'bar',
        data: data,
        options: options
    });
    };
};