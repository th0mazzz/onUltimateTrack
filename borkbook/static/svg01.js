var p = document.getElementById("vimage");

var clrbut = document.getElementById("but_clear");

var prevx;
var prevy;

var clear = function() {
    prevx=NaN;
    prevy=NaN;
    p.innerHTML=""
}

var circle = function(x, y) {
    var c = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    c.setAttribute("cx", x);
    c.setAttribute("cy", y);
    c.setAttribute("r", 10);
    c.setAttribute("fill", "red");
    c.setAttribute("stroke", "black");
    p.appendChild(c);
}

var line = function(x1, y1, x2, y2) {
    var l = document.createElementNS("http://www.w3.org/2000/svg", "line");
    l.setAttribute("x1", x1);
    l.setAttribute("y1", y1);
    l.setAttribute("x2", x2);
    l.setAttribute("y2", y2);
    l.setAttribute("stroke", "black");
    p.appendChild(l);
}

var draw = function(e) {
    var x = e.offsetX;
    var y = e.offsetY; 
    if (isNaN(prevx) && isNaN(prevy)) {
	circle(x, y);
    }
    else {
	line(prevx, prevy, x, y);
	circle(x,y);
    }
    prevx=x;
    prevy=y;
}

clrbut.addEventListener('click', clear);
p.addEventListener('click', draw);
