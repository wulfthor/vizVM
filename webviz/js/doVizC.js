function loadData(datafile) {

  var inputfile = datafile;
  generateVis(inputfile);
}

function generateVis(ds) {
  var margin = {top: 30, right: 20, bottom: 30, left: 50},
      width = 900 - margin.left - margin.right,
      height = 870 - margin.top - margin.bottom;

  // Parse the date / time
  var parseDate = d3.time.format("%d-%m-%Y %H:%M:%S").parse;
  var color = d3.scale.category20();


  // Set the ranges
  var x = d3.time.scale().range([0, width]);
  var y = d3.scale.linear().range([height, 0]);

  // Define the axes
  var xAxis = d3.svg.axis().scale(x)
    .orient("bottom").ticks(5);

  var yAxis = d3.svg.axis().scale(y)
    .orient("left").ticks(5);

  // Define the line
  var rwline = d3.svg.line()
    .defined(function(d) { return d.kbs != null; })
    .x(function(d) { return x(d.ts); })
    .y(function(d) { return y(d.kbs); });

  // Adds the svg canvas
  var svg = d3.select("body")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  // Get the data, +d turns it into a number
  d3.csv(ds, function(error, data) {
    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "ts"; }));
    data.forEach(function(d) {
      d.ts = parseDate(d.ts);
      d.kbs = +d.kbs;
    });

    // Scale the range of the data
    x.domain(d3.extent(data, function(d) { return d.ts; }));
    y.domain([0, d3.max(data, function(d) { return d.kbs; })]); 

    // Nest the entries by symbol
    var dataNest = d3.nest()
    .key(function(d) {return d.vm;})
    .entries(data);

  // Loop through each symbol / key
  var count = 0;
  dataNest.forEach(function(d) {
    count++;
    console.log("K: " + d.key);
    svg.append("path")
    .attr("class", "line")
    .style("stroke", function() {
      return d.color = color(d.key);})
    .attr("d", rwline(d.values));

  svg.append("rect")
    .attr("x", 100)
    .attr("y", 50 + (15 * count))
    .attr("width", 45)
    .attr("height", 10)
    .style("fill", color(d.key));
  svg.append("text")
    .attr("x", 150 )
    .attr("y", 56 + (15 * count))
    .text(d.key)
    .attr("fill", "black")
    .attr("text-anchor", "top");

  });

  //

  // Add the X Axis
  svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);

  // Add the Y Axis
  svg.append("g")
    .attr("class", "y axis")
    .call(yAxis);

  });
}

