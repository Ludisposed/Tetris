var stage;
var SIZE = 10;
var currentBlock;
var lvl;

var Game = {
    SPEED : 16,
    frameNumber : 0,
    GAMEOVER : false,
    lineCount : 0
};

var colors = [
                 { nr: 0, color: [ 0, 0, 0] },       // black
                 { nr: 1, color: [ 255, 255, 255] }, // white
                 { nr: 2, color: [ 255, 0, 0] },     // red
                 { nr: 3, color: [ 0, 255, 0] },     // green
                 { nr: 4, color: [ 0, 0, 255] },     // blue
                 { nr: 5, color: [ 0, 255, 255] },   // light blue
                 { nr: 6, color: [ 255, 255, 0] },   // yellow
                 { nr: 7, color: [ 255, 0, 255] },   // purple
             ];


var BLOCKS = [           
                 { color: 1, coordinates:  
                     [
                         { x: 0, y: 0 },
                         { x: 0, y: -1 },
                         { x: 0, y: 1 },
                         { x: 1, y: 1 }
                     ]
                 }, { color: 2, coordinates: 
                     [
                         { x: 0, y: 0 },
                         { x: 0, y: -1 },
                         { x: 0, y: 1 },
                         { x: -1, y: 1 }
                     ]
                 }, { color: 3, coordinates:
                     [
                         { x: 0, y: 0 },
                         { x: 1, y: 0 },
                         { x: 0, y: 1 },
                         { x: -1, y: 1 }
                     ]
                 }, { color: 4, coordinates:
                     [
                         { x: 0, y: 0 },
                         { x: -1, y: 0 },
                         { x: 0, y: 1 },
                         { x: 1, y: 1 }
                     ]
                 }, { color: 5, coordinates:
                     [
                         { x: 0, y: 0 },
                         { x: 0, y: 1 },
                         { x: 1, y: 0 },
                         { x: 1, y: 1 }
                     ]
                 }, { color: 6, coordinates:
                     [
                         { x: 0, y: -1 },        
                         { x: 0, y: 0 },
                         { x: 0, y: 1 },
                         { x: 0, y: 2 }
                     ]
                 }, { color: 7, coordinates: 
                     [
                         { x: 0, y: -1 },            
                         { x: 0, y: 0 },
                         { x: -1, y: 0 },
                         { x: 1, y: 0 }
                     ]
                 }
             ]

function newBlock() {
    var rnd = Math.floor((Math.random()*7))
    return BLOCKS[rnd]
}

/* class: Block
 *     args: 
 *         this.color : a color in (int)
 *         this.coordinates : a list of { diffx, diffy }
 *
 *     functions:
 *         create(x, y): create a new block on position (x, y)
 *         rotations: Left, Right, **
 *         move{direc}: Left, Right, Down
 *         {Add/Remove}ToStage: Removes or adds the block to the stage
 *         getPosition: Gets the position of the Block
 *         getColour: Gets the colour of the block
 */
var Block = function(block) {
    var that = {};    
    var position = {
        x : 0,
        y : 0
    };
    var blockDefinitions = [];
    var blockContainer = {};

    that.create = function(x, y) {            
        blockContainer = new createjs.Container();
        for (key in block.coordinates) {
            var p = {
                x: block.coordinates[key].x,
                y: block.coordinates[key].y
            }
            blockDefinitions.push(p);
        }

        position.x = x;
        position.y = y;
        blockContainer.x = x * SIZE + 0.5 * SIZE;
        blockContainer.y = y * SIZE + 0.5 * SIZE;    
        blockContainer.rotation = 0;
        for (key in blockDefinitions) {    
            var g = new createjs.Graphics();
            var r = blockDefinitions[key];
            g.beginStroke(createjs.Graphics.getRGB(0,0,0));            
            var color = colors[block.color].color;
            g.beginFill(createjs.Graphics.getRGB(color[0], color[1], color[2]));            
            g.drawRect(r.x * SIZE - 0.5 * SIZE, r.y * SIZE - 0.5 * SIZE, SIZE, SIZE);        
            blockContainer.addChild(new createjs.Shape(g));    
        }
    };
    
    that.rotateLeft =  function () {
        this.rotate(90);    
        for (key in blockDefinitions) {
            var x_tmp = blockDefinitions[key].x;
            blockDefinitions[key].x = blockDefinitions[key].x * 0 + blockDefinitions[key].y * -1;    
            blockDefinitions[key].y = x_tmp * 1 + blockDefinitions[key].y * 0;                
        };    
    };
    
    that.rotateRight =  function () {
        this.rotate(270);
        for (key in blockDefinitions) {
            var x_tmp = blockDefinitions[key].x;
            blockDefinitions[key].x = blockDefinitions[key].x * 0 + blockDefinitions[key].y * 1;    
            blockDefinitions[key].y = x_tmp * -1 + blockDefinitions[key].y * 0;            
        };            
    };
    
    that.rotate = function(angle) {                        
        blockContainer.rotation += angle;        
    };
    
    that.addToStage = function() {
        stage.addChild(blockContainer);            
    };
    
    that.removeFromStage = function() {
        blockContainer.removeAllChildren();
        stage.removeChild(blockContainer);    
    };
    
    that.moveDown = function() {
        position.y += 1;
        blockContainer.y += SIZE;            
    };
    
    that.moveLeft = function() {
        position.x -= 1;
        blockContainer.x -= SIZE;            
    };
    
    that.moveRight = function() {
        position.x += 1;
        blockContainer.x += SIZE;            
    };

    that.getBlockRotatePositions = function(left){
        var positions = [];

        for (key in blockDefinitions) {
            var p = {
                x: blockDefinitions[key].x * 0 + blockDefinitions[key].y * -1 * left + position.x,
                y: blockDefinitions[key].x * 1 * left + blockDefinitions[key].y * 0 + position.y
            };
            positions.push(p);                
        }
        return positions

    }
    
    that.getBlockPositions = function(xLookAhead, yLookAhead) {
        var positions = [];
        for (key in blockDefinitions) {
            var p = {
                x: blockDefinitions[key].x + position.x + xLookAhead, 
                y: blockDefinitions[key].y + position.y + yLookAhead 
            };
            positions.push(p);    
        }        
        return positions;
    };
    
    that.getColorNr = function() {
        return block.color;
    };
    
    return that;
}


var Level = function () {
    var WIDTH = 10;
    var HEIGHT = 20;
    var BLOCKDIMENSION = 10;
    var matrix = [];
    var fallenBlocks = {};
    var that = {}

    var add = function(a, b) {
        return a+b;    
    }

    that.create = function () {
        var a, i, j;
        for (i = 0; i < HEIGHT + 1; i += 1) {
            a = [];
            for (j = 0; j < WIDTH + 2; j += 1) {
                if (j === 0 || j === WIDTH + 1 || i === HEIGHT) {
                    a[j] = 1;
                }
                else {
                    a[j] = 0;
                }
            }
            matrix[i] = a;
        }
        fallenBlocks = new createjs.Container();
        stage.addChild(fallenBlocks);
    };

    that.addToStage = function () {
        var i,j;
        var g = new createjs.Graphics();
        for (i = 0; i < HEIGHT + 1; i += 1) {
            for (j = 0; j < WIDTH + 2; j += 1) {
                if (matrix[i][j] >= 1) {
                    var color = colors[matrix[i][j]].color;
                    g.beginStroke(createjs.Graphics.getRGB(0,0,0));
                    g.beginFill(createjs.Graphics.getRGB(color[0],color[1],color[2]));
                    g.drawRect(j * BLOCKDIMENSION, i * BLOCKDIMENSION, BLOCKDIMENSION, BLOCKDIMENSION);
                    fallenBlocks.addChild(new createjs.Shape(g));
                }
            }
        }
        fallenBlocks.cache(0,0, 120, 210);
    };

    that.redraw = function () {
        fallenBlocks.removeAllChildren();
        stage.removeChild(fallenBlocks);

        g = {};
        g = new createjs.Graphics();
        fallenBlocks = {};
        fallenBlocks = new createjs.Container();
        this.addToStage();

        stage.addChild(fallenBlocks);
    };

    that.addBlock = function(block) {
        var i;
        var g = new createjs.Graphics();
        var positions = block.getBlockPositions(0,0);
        var colorNr = colors[block.getColorNr()].nr;
        var color = colors[block.getColorNr()].color;
        for (i = 0; i < positions.length; i += 1) {
            matrix[positions[i].y][positions[i].x] = colorNr;
            g.beginStroke(createjs.Graphics.getRGB(0,0,0));
            g.beginFill(createjs.Graphics.getRGB(color[0],color[1],color[2]));
            g.drawRect(positions[i].x * BLOCKDIMENSION, positions[i].y * BLOCKDIMENSION, BLOCKDIMENSION, BLOCKDIMENSION);
            fallenBlocks.addChild(new createjs.Shape(g));
        }
        fallenBlocks.cache(0,0, 120, 210);
    };

    that.getMatrix = function() {
        return matrix;
    };

    that.printMatrix = function() {
        var i,j;
        for (i = 0; i < HEIGHT; i += 1) {
            console.log(matrix[i]);
        }
    };

    that.collision = function(blockPositions) {
        var i;
        for (i = 0; i < blockPositions.length; i += 1) {
            if (matrix[blockPositions[i].y][blockPositions[i].x] >= 1) {
                if (blockPositions[i].y === 0) {
                    return 2;
                }
                else {
                    return 1;
                }
            }
        }
        return 0;
    };

    that.checkLines = function() {
        var i,j;
        var lines = 0;
        var firstClearedLine = 19;
        for (i = 0; i < HEIGHT; i += 1) {
            var lineHasToBeCleared = true;
            for (j = 1; j < WIDTH + 1; j += 1) {
                if (matrix[i][j] === 0) {
                    lineHasToBeCleared = false;
                    break;
                }
            }
            if (lineHasToBeCleared === true) {
                this.clearLine(i);
                lines += 1;
                firstClearedLine = Math.min(firstClearedLine, i);
            }
        }
        if (lines > 0) {
            this.moveLinesDown(lines, firstClearedLine);
            this.redraw();
        }
        return lines;
    };


    that.clearLine = function(lineNr) {
        var i;
        for (i = 1; i < WIDTH + 1; i += 1) {
            matrix[lineNr][i] = 0;
        }
    };

    that.moveLinesDown = function(nrOfLines, lineNr) {
        var i,j;
        var lines = [];
        for (i = lineNr - 1; i >= 0; i -= 1) {
            var sum = matrix[i].reduce(add, 0);
            if (sum > 2) {
                for (j = 1; j < WIDTH + 1; j += 1) {
                    matrix[i+nrOfLines][j] = matrix[i][j];
                }
                this.clearLine(i);
            }
        }
    };

    return that;
};

function init() {
    document.onkeydown = handleKeyDown;
    stage = new createjs.Stage("TetrisCanvas");
    createjs.Ticker.on("tick", tick);    
    createjs.Ticker.setFPS(30);
    lvl = Level()
    lvl.create()
    lvl.addToStage()
    startGame()
}

function handleKeyDown(event) {
    switch(event.keyCode) {
        case 37:
            var posLookAhead = currentBlock.getBlockPositions(-1,0);
            var collision = lvl.collision(posLookAhead);

            if (collision === 0) {
                currentBlock.moveLeft();
            }
            break;
        case 38:
            var posRotate = currentBlock.getBlockRotatePositions(1)
            var collision = lvl.collision(posRotate)
            
            if (collision === 0) {
                currentBlock.rotateLeft();
            }
            break;
        case 39:
            var posLookAhead = currentBlock.getBlockPositions(1,0);
            var collision = lvl.collision(posLookAhead);

            if (collision === 0) {
                currentBlock.moveRight();
            }
            break;
        case 40:
            var posLookAhead = currentBlock.getBlockPositions(0,1);
            var collision = lvl.collision(posLookAhead);

            if (collision === 0) {
                currentBlock.moveDown();
            }
            break;
        default:
            break;
    }
}

function startGame() {
    currentBlock = Block(newBlock());
    currentBlock.create(5, 1);
    currentBlock.addToStage();
}

function tick(event) {
    if (Game.GAMEOVER === false) {
        Game.frameNumber += 1;
        if (Game.frameNumber % Game.SPEED === 0) {
            var posLookAhead = currentBlock.getBlockPositions(0,1);
            var collision = lvl.collision(posLookAhead);
            Game.LineCount += lvl.checkLines();
            
            if (collision === 0) {
                currentBlock.moveDown();
            }        
     
            if (collision >= 1) {
                
                lvl.addBlock(currentBlock);
                currentBlock.removeFromStage();        
                currentBlock = Block(newBlock());
                currentBlock.create(5, 1);
                pos = currentBlock.getBlockPositions(0, 0);
                if (lvl.collision(pos) === 0) {
                    currentBlock.addToStage();
                } else {
                     Game.GAMEOVER = true;
                }
            }
        }
    }

    stage.update(event);
}
