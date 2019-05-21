var getSVGObjects = function(){
  var nodes = Array.prototype.slice.call(svg[0][0].childNodes)
  var bigboy = {};
  for (i = 1; i < nodes.length; i++){
    /*
    inspect class of each SVG Obj
    if line it is a path
    if circle it is a circle
    if x it is a x
    */

    bigboy[`path${i}`] = nodes[i].getAttribute('d');
  }
  bigboy['circle1'] = JSON.stringify({'cx':12, 'cy':12})
  return bigboy;
}


var yeet = function(){
  var dataRows = getSVGObjects();
  var xhttp = new XMLHttpRequest();
  var query = "?";
  Object.entries(dataRows).forEach(function([key, value]){
    console.log(key, value)
    query += `${key}=${value}&`
  });

  console.log(query);
  xhttp.open("GET", "/yeet" + query, true);
  xhttp.send();

}

save.addEventListener('click',yeet)

// based on http://bl.ocks.org/cloudshapes/5661984 by cloudshapes

var margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;


// var npoints = 100;
var ptdata = [];
var session = [];
var path;
var drawing = false;

var output = d3.select('#output');

var line = d3.svg.line()
    .interpolate("bundle") // basis, see http://bl.ocks.org/mbostock/4342190
    .tension(1)
    .x(function(d, i) { return d.x; })
    .y(function(d, i) { return d.y; });

var svg = d3.select("#sketch").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)


svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg
  .on("mousedown", listen)
  .on("touchstart", listen)
  .on("touchend", ignore)
  .on("touchleave", ignore)
  .on("mouseup", ignore)
  .on("mouseleave", ignore);


// ignore default touch behavior
var touchEvents = ['touchstart', 'touchmove', 'touchend'];
touchEvents.forEach(function (eventName) {
  document.body.addEventListener(eventName, function(e){
    e.preventDefault();
  });
});


function listen () {
  drawing = true;
  output.text('event: ' + d3.event.type);
  ptdata = []; // reset point data
  path = svg.append("path") // start a new line
    .data([ptdata])
    .attr("class", "line")
    .attr("d", line);

  if (d3.event.type === 'mousedown') {
    svg.on("mousemove", onmove);
  } else {
    svg.on("touchmove", onmove);
  }
}

function ignore () {
  var before, after;
  output.text('event: ' + d3.event.type);
  svg.on("mousemove", null);
  svg.on("touchmove", null);

  // skip out if we're not drawing
  if (!drawing) return;
  drawing = false;

  before = ptdata.length;
  console.group('Line Simplification');
  console.log("Before simplification:", before)

  after = ptdata.length;

  console.log("After simplification:", ptdata.length)
  console.groupEnd();

  var percentage = parseInt(100 - (after/before)*100, 10);
  output.html('Points: ' + before + ' => ' + after + '. <b>' + percentage + '% simplification.</b>');

  // add newly created line to the drawing session
  session.push(ptdata);

  // redraw the line after simplification
  tick();
}


function onmove (e) {
  var type = d3.event.type;
  var point;

  if (type === 'mousemove') {
    point = d3.mouse(this);
    output.text('event: ' + type + ': ' + d3.mouse(this));
  } else {
    // only deal with a single touch input
    point = d3.touches(this)[0];
    output.text('event: ' + type + ': ' + d3.touches(this)[0]);
  }

  // push a new data point onto the back
  ptdata.push({ x: point[0], y: point[1] });
  tick();
}

function tick() {
  path.attr("d", function(d) { return line(d); }) // Redraw the path:
}
