var stage, circle;
var lvl = {};

blocks = Something

function init() {
    stage = new createjs.Stage("TetrisCanvas");
    createjs.Ticker.on("tick", tick);    
    createjs.Ticker.setFPS(30);
    
    startGame()
}



// DEMO CODE
function startGame() {
    circle = new createjs.Shape();
    circle.graphics.beginFill("DeepSkyBlue").drawCircle(0, 0, 50);
    circle.y = 100;
    stage.addChild(circle);
}

function tick(event) {
    circle.y += 10;
    stage.update(event);
}
