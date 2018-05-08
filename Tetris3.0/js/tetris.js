var stage;
var lvl = {};

// blocks = Something

function init() {
    stage = new createjs.Stage("TetrisCanvas");
    createjs.Ticker.addListener(window);    
    createjs.Ticker.useRAF = true;
    createjs.Ticker.setFPS(60);
    
    startGame()
}

// DEMO CODE
function startGame() {
    circle.graphics.beginFill("DeepSkyBlue").drawCircle(0, 0, 50);
    circle.x = 100;
    circle.y = 100;
    stage.addChild(circle);
}

function tick() {
    circle = stage.getChildByName("circle");
    circle.y -= 10;
    stage.update();
}
