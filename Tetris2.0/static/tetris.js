/*
* @Author: Li Qin
* @Date:   2018-05-06 22:44:51
* @Last Modified by:   Li Qin
* @Last Modified time: 2018-05-07 00:55:47
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

document.onLoad = initial()

function initial() {
    updateScore();
    output();
    
}
function updateScore() {
    var scoreDetails = document.getElementById("score");
    var html = "<br/><br/><h2>&nbsp;</h2><h2>Score: " + score + "</h2>";

    html = replaceAll(replaceAll(replaceAll(html, "&nbsp;,", "&nbsp;&nbsp;"), ",&nbsp;", "&nbsp;&nbsp;"), ",", "&nbsp;");
    scoreDetails.innerHTML = html;

}

function output() {
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
    output.innerHTML = html;
}

function replaceAll(target, search, replacement) {
    return target.replace(new RegExp(search, 'g'), replacement);
 }