/*
---------------------------------------
THIS SECTION IS FOR SENDING SVG OBJECTS TO PYTHON
---------------------------------------
*/

var getSVGObjects = function(){
  var nodes = Array.prototype.slice.call(svg[0][0].childNodes)
  var objects = {};
  console.log(nodes)
  for (i = 0; i < nodes.length; i++){
    /*
    inspect class of each SVG Obj
    if line it is a path
    if click-circle it is a circle
    */
    if (nodes[i].className){
      if (nodes[i].className.baseVal == "line"){
        objects[`path${i}`] = nodes[i].getAttribute("d")
      } else if (nodes[i].className.baseVal == "click-circle"){
        objects[`click-circle${i}`] = JSON.stringify({"cx":nodes[i].getAttribute("cx"),"cy":nodes[i].getAttribute("cy"), "r":nodes[i].getAttribute("r"), "fill":nodes[i].getAttribute("fill")});
      }
    }
  }
  return objects;
}

var hideWarning = function(){
  document.getElementById("alert").style.visibility="hidden";
}


// sends attributes of SVG objects to Python as Strings
var sendSVGObjects = function(){
  var name = document.getElementById("playname").value.trim(); // name of the play
  var id = document.getElementById("id").value.trim(); // id of team
  console.log(id);
  if (name.length > 0){
    var dataRows = getSVGObjects(); // dictionary of SVG objects
    var xhttp = new XMLHttpRequest();
    var query = "?";
    Object.entries(dataRows).forEach(function([key, value]){
      query += `${key}=${value}&`
    });
    query +=`name=${name}&id=${id}`
    xhttp.onreadystatechange = function(){
      if (this.readyState == 4 && this.status == 200){
        // change alert to successful message!
        var alert = document.getElementById("alert");
        alert.className = "row justify-content-center mt-2 text-success";
        alert.innerHTML = "Success! Redirecting to previous team page..."
        alert.style.visibility = "visible";
        setTimeout(function(){window.location.href=`/team?team=${id}`}, 2000)
      }
    };
    xhttp.open("GET", "/receiveObjects" + query, true);
    xhttp.send();
  } else{
    // shows alert
    document.getElementById("alert").style.visibility = "visible";
    // hide alert after 1 second
    setTimeout("hideWarning()", 1000)
  }
};

var saveBtn = document.getElementById('submit')
saveBtn.addEventListener('click', sendSVGObjects)

/*
---------------------------------------
THIS SECTION IS FOR SVG
---------------------------------------
*/

var margin = {top: 0, right: 0, bottom: 0, left: 0},
    width = 1200 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;


// var npoints = 100;
var ptdata = [];
var session = [];
var path;
var drawing = false;
var color = "";


var line = d3.svg.line()
    .interpolate("bundle") // basis, see http://bl.ocks.org/mbostock/4342190
    .tension(1)
    .x(function(d, i) { return d.x; })
    .y(function(d, i) { return d.y; });

// select SVG canvas
var svg = d3.select("#sketch");
var output = d3.select("#output");

svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // assign fxns to SVG for drawing
svg
  .on("mousedown", listen)
  .on("touchstart", listen)
  .on("touchend", ignore)
  .on("touchleave", ignore)
  .on("mouseup", ignore)
  .on("mouseleave", ignore);

/*
---------------------------------------
THIS SECTION IS FOR UTILITY BUTTONS
---------------------------------------
*/
// check if Object is path or circle
var checkObject = function(child){
  if (child.className){
    if (child.className.baseVal == "line"){
      return true;
    }
    if (child.className.baseVal == "click-circle"){
      return true;
    }
  };
  return false;

};

var undoStack = [];

var undoBtn = document.getElementById("undo");

var undo = function(e){
    var canvas = svg[0][0];
    if (checkObject(canvas.lastChild)){
      // remove the last child and pushes to undoArray
      undoStack.push(canvas.removeChild(canvas.lastChild));
    }
};

var redoBtn = document.getElementById("redo");

var redo = function(e){
    var canvas = svg[0][0];
    var lastObj = undoStack.pop();
    console.log(lastObj);
    canvas.appendChild(lastObj);
};

var clearBtn = document.getElementById("clear");


// removes all paths and circles from svg
var clear = function(e){
    var canvas = svg[0][0]
    children = canvas.childNodes;
    console.log(children);
    for (i = 0; i < children.length; i++){
      console.log(i, checkObject(children[i]));
      if (checkObject(children[i])){
        canvas.removeChild(children[i]);
        i -= 1;
      }
    };
    console.log(children);
};

undoBtn.addEventListener('click', undo);
redoBtn.addEventListener('click', redo);
clearBtn.addEventListener('click', clear);

/*
---------------------------------------
THIS SECTION IS FOR CIRCLES
---------------------------------------
*/


var isLine = true;
var isCircle = false;
var isBlue = true;

// get circle buttons on menu
var redCircle = document.getElementById("red-circle");
var blueCircle = document.getElementById("blue-circle");
var linebtn = document.getElementById("linebtn");

var toggleBlue = function() {
  isLine = false;
  isCircle = true;
  isBlue = true;
}

var toggleRed = function() {
  isLine = false;
  isCircle = true;
  isBlue = false;
}

var toggleLine = function() {
  isLine = true;
  isCircle = false;
}

redCircle.addEventListener("click", toggleRed);

blueCircle.addEventListener("click", toggleBlue);

linebtn.addEventListener("click", toggleLine);

function draw_circle(x, y) {
  if (isCircle) {
    if (isBlue) {
      svg.append("circle")
        .attr('class', 'click-circle')
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 20)
        .attr("fill", "blue");
      }
    else {
      svg.append("circle")
        .attr('class', 'click-circle')
        .attr("cx", x)
        .attr("cy", y)
        .attr("r", 20)
        .attr("fill", "red");
    }
  }
}

/*
---------------------------------------
THIS SECTION IS FOR CURVED PATH DRAWING
---------------------------------------
*/
// based on http://bl.ocks.org/cloudshapes/5661984 by cloudshapes





// ignore default touch behavior
var touchEvents = ['touchstart', 'touchmove', 'touchend'];
touchEvents.forEach(function (eventName) {
  document.body.addEventListener(eventName, function(e){
    e.preventDefault();
  });
});


function listen () {
  if (isLine) {
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
else if (isCircle) {
  svg.on("click", function() {
    var coords = d3.mouse(this);
    console.log(coords);
    draw_circle(coords[0], coords[1]);
  });
  }
}

function ignore () {
  if (isLine) {
    var before, after;
    output.text('event: ' + d3.event.type);
    svg.on("mousemove", null);
    svg.on("touchmove", null);

    // skip out if we're not drawing
    if (!drawing) return;
    drawing = false;

    // SCRAP Simplification
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
}

function onmove (e) {
  if (isLine) {
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
}

function tick() {
  if (isLine) {
    path.attr("d", function(d) { return line(d); }) // Redraw the path:
  }
}
