function init() {
    var stage = new createjs.Stage("TetrisCanvas");

    // Demo Code on how to use the canvas!
    var circle = new createjs.Shape();
    circle.graphics.beginFill("DeepSkyBlue").drawCircle(0, 0, 50);
    circle.x = 100;
    circle.y = 100;
    stage.addChild(circle);
    stage.update()
}
