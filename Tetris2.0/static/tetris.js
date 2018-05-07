/*
* @Author: Li Qin
* @Date:   2018-05-06 22:44:51
* @Last Modified by:   Li Qin
* @Last Modified time: 2018-05-07 11:56:49
*/
var grid = [
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
[0,0,0,0,0,0,0,0,0,0],
];

//Block shapes
var shapes = {
    I: [[0,0,0,0], [1,1,1,1], [0,0,0,0], [0,0,0,0]],
    J: [[2,0,0], [2,2,2], [0,0,0]],
    L: [[0,0,3], [3,3,3], [0,0,0]],
    O: [[4,4], [4,4]],
    S: [[0,5,5], [5,5,0], [0,0,0]],
    T: [[0,6,0], [6,6,6], [0,0,0]],
    Z: [[7,7,0], [0,7,7], [0,0,0]]
};

var score = 0;
//Block colors
var colors = ["F92338", "C973FF", "1C76BC", "FEE356", "53D504", "36E0FF", "F8931D"];

var currentShape = {x:0, y:0, shape:undefined};
var upcomingShape = undefined;

document.onLoad = initial();

function initial() {
    update();
}

//keycode w:87 a:65 s:83 d:68 up:38 down:40 left:37 right:39
window.onkeydown = function (event) {
    var characterPressed = String.fromCharCode(event.keyCode);
    if (event.keyCode == 38 || event.keyCode == 87) {
        rotateShape();
    } else if (event.keyCode == 37 || event.keyCode == 65) {
        moveLeft();
    } else if (event.keyCode == 39 || event.keyCode == 68) {
        moveRight();
    } else if (event.keyCode == 40 || event.keyCode == 83) {
        moveDown();
    }
    updateGrid();
}

function rotateShape() {

}

function moveDown() {
    removeShape();
    currentShape.y++;
    if (collides(grid, currentShape)) {
        currentShape.y--;
    }
    applyShape();
}

function moveLeft() {
    removeShape();
    currentShape.x--;
    if (collides(grid, currentShape)) {
        currentShape.x++;
    }
    applyShape();
}

function moveRight() {
    removeShape();
    currentShape.x++;
    if (collides(grid, currentShape)) {
        currentShape.x--;
    }
    applyShape();
}

function cleanLine(){
    cleaned = 0
    for (var row = 0; row < currentShape.shape.length; row++) {
        if (currentShape.shape[row].every(function (item) {return item === 1;})) {
            cleaned++;
        }
    }
}

function update(){
    updateScore();
    updateGrid();
    if (upcomingShape === undefined) {
        upcomingShape = randomShape(shapes)
    }
    nextShape() 
}

function updateGrid() {
    var output = document.getElementById('output');
    var html = "<h1>Tetris</h1>var grid = [";
    var space = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
    for (var i = 0; i < grid.length; i++) {
        if (i === 0) {
            html += "[" + grid[i] + "]";
        } else {
            html += "<br/>" + space + "[" + grid[i] + "]";
        }
    }
    html += "];";
    for (var c = 0; c < colors.length; c++) {
        html = replaceAll(html, "," + (c + 1), ",<font color=\"" + colors[c] + "\">" + (c + 1) + "</font>");
        html = replaceAll(html, (c + 1) + ",", "<font color=\"" + colors[c] + "\">" + (c + 1) + "</font>,");
    }
    output.innerHTML = html;
}

function updateScore() {
    var scoreDetails = document.getElementById("score");
    var html = "<br/><br/><h2>&nbsp;</h2><h2>Score: " + score + "</h2>";

    html = replaceAll(replaceAll(replaceAll(html, "&nbsp;,", "&nbsp;&nbsp;"), ",&nbsp;", "&nbsp;&nbsp;"), ",", "&nbsp;");
    scoreDetails.innerHTML = html;

}

function nextShape() {
    currentShape.shape = upcomingShape;
    currentShape.x = Math.floor(grid[0].length / 2) - Math.ceil(currentShape.shape[0].length / 2);
    currentShape.y = 0;
    upcomingShape = randomShape(shapes)
}

function applyShape() {
    for (var row = 0; row < currentShape.shape.length; row++) {
        for (var col = 0; col < currentShape.shape[row].length; col++) {
            if (currentShape.shape[row][col] !== 0){
                grid[currentShape.y + row][currentShape.x + col] = currentShape.shape[row][col];
            }
        }
    }
}

function removeShape() {
    for (var row = 0; row < currentShape.shape.length; row++) {
        for (var col = 0; col < currentShape.shape[row].length; col++) {
            if (currentShape.shape[row][col] !== 0) {
                grid[currentShape.y + row][currentShape.x + col] = 0;
            }
        }
    }
}

function randomShape(obj) {
    return(obj[randomKey(obj)])
}

function randomKey(obj) {
    var keys = Object.keys(obj);
    i = Math.floor(Math.random() * keys.length)
    return keys[i]
}

function replaceAll(target, search, replacement) {
    return target.replace(new RegExp(search, 'g'), replacement);
}

function collides(scene, object) {
    for (var row = 0; row < object.shape.length; row++){
        for (var col = 0; col < object.shape[row].length; col++){
            if (object.shape[row][col] !== 0) {
                if (scene[object.y + row] === undefined || scene[object.y + row][object.x + col] === undefined || scene[object.y + row][object.x + col] !== 0){
                    return true
                }
            }
        }
    }
    return false
}
