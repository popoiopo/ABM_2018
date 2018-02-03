var ChartModule = function(canvas_width, canvas_height) {

    // Create the tag:
    var canvas_tag = "<canvas id='line_canvas' style='margin-top:20px;' width='" + canvas_width + "' height='" + canvas_height + "' ";
    canvas_tag += "></canvas>";
    // Append it to body:
    var canvas = $(canvas_tag)[0];
    $("#elements1").append(canvas);
    // Create the context and the drawing controller:
    var context = canvas.getContext("2d");

    // Prep the chart properties and series:
    var datasets = [{
        label: "Average waitingtime",
        strokeColor: "rgba(220,220,220,1)",
        pointColor: "rgba(220,220,220,1)",
        pointStrokeColor: "#fff",
        pointHighlightFill: "#fff",
        pointHighlightStroke: "rgba(220,220,220,1)",
        data: [],
        backgroundColor: "rgba(153,255,51,0.4)"
    }];

    var data = {
        datasets: datasets
    };

    //  var data = {
    //     labels: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    //     datasets: [
    //         {
    //             label: "Prime and Fibonacci",
    //             fillColor: "rgba(220,220,220,0.2)",
    //             strokeColor: "rgba(220,220,220,1)",
    //             pointColor: "rgba(220,220,220,1)",
    //             pointStrokeColor: "#fff",
    //             pointHighlightFill: "#fff",
    //             pointHighlightStroke: "rgba(220,220,220,1)",
    //             data: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    //         },
    //         {
    //             label: "My Second dataset",
    //             fillColor: "rgba(151,187,205,0.2)",
    //             strokeColor: "rgba(151,187,205,1)",
    //             pointColor: "rgba(151,187,205,1)",
    //             pointStrokeColor: "#fff",
    //             pointHighlightFill: "#fff",
    //             pointHighlightStroke: "rgba(151,187,205,1)",
    //             data: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    //         }
    //     ]
    // };

    // var options = { };

    // // Create the chart object
    // var chart = new Chart(context, {
    //     type: 'line',
    //     data: data,
    //     options: options
    // });

    var chart = new Chart(context, {
      type: 'line',
      data: data
    });

    this.render = function(data) {
      console.log(data);
      console.log(chart.data);
        chart.data.datasets[0].data = data;
        console.log(chart.data.datasets[0].data);
        chart.update();
    };

    this.reset = function() {
        chart.destroy();
        var chart = new Chart(context, {
          type: 'line',
          data: data
        });
    };
};