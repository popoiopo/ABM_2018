var d3viz = function(vars) {
  console.log(vars)
  vars = [{"Beers" : [3,2,1,2,44,2,2,5,2], "SomethingElse" : [2,23,2,4,2,4], "WaitingTime" : [23,2,42,2,14,2]}];
  var width = 600,
      height = 150,
      distX = width / (vars.length + 1);

  var svg = d3.select("#elements").append("svg")
    .attr("width", width)
    .attr("height", height);

  var circle = svg.selectAll("g")
    .data(vars)
    .enter()
      .append("g")
        .attr("transform", function(d, i){ return "translate("+ (i+1) * distX + ", "+ height / 2 + ")"; })
        .data(vars)
        .on("click", function(d, i){ drawChart(d);});

  circle.append("circle")
    .attr("cx",  0)
    .attr("cy", 0)
    .attr("r", height / 2)
    .style("fill", "red");

  circle.append("text")
    .attr("text-anchor", "middle")
    .text(function(d, i) {return Object.keys(vars[i])[0]} )
    .style("fill", "white")
    .style("font-size", "1em")
    .style("font-weight", "bold");

  this.render = function(data) {
      console.log(data);
      // updateChart(data);
      // console.log("hallooooooo#########");
  };

  this.reset = function() {
    // console.log("halloooopoapdsaeughbuvbo83h6o863;")
  };

  function drawChart (data) {
  d3.select(".linegraph").remove();
  var keydata = Object.keys(data)[0];
  var real_data = data[keydata];
  var N = real_data.length;
  var scaling = Array.apply(null, {length: N}).map(Number.call, Number);

  var margin = {top: 20, right: 20, bottom: 30, left: 50},
      width = 600 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

  var x = d3.scaleLinear()
      .domain(d3.extent(scaling, function(d) { return d; }))
      .range([0, width]);

  var y = d3.scaleLinear()
      .domain(d3.extent(real_data, function(d) { return d; }))
      .rangeRound([height, 0]);

  var line = d3.line()
      .x(function(d, i) { return x(i); })
      .y(function(d) { return y(d); });

  var svg = d3.select("#elements").append("svg")
      .attr("class", "linegraph")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom);

  var g = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  g.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).ticks(real_data.length - 1))
    .select(".domain")
      .remove();

  g.append("g")
      .attr("class", "y axis")
      .call(d3.axisLeft(y))
    .append("text")
      .attr("fill", "#000")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", "0.71em")
      .attr("text-anchor", "end")
      .text(keydata);

  g.append("path")
      .datum(real_data)
      .attr("class", "line")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-linejoin", "round")
      .attr("stroke-linecap", "round")
      .attr("stroke-width", 1.5)
      .attr("d", line);

    function updateChart (data) {
      var keydata = Object.keys(data)[0];
      var real_data = data[keydata];

      x.domain(d3.extent(scaling, function(d) { return d; }));
      y.domain(d3.extent(real_data, function(d) { return d; }));

      var svg = d3.select(".linegraph").transition();
      svg.select(".line")   // change the line
          .duration(750)
          .attr("d", line(real_data));
      svg.select(".x.axis") // change the x axis
          .duration(750)
          .call(xAxis);
      svg.select(".y.axis") // change the y axis
          .duration(750)
          .call(yAxis);
    }
  }
};

