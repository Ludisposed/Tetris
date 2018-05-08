var stage;
var SIZE = 10;

var colors = [
		{nr: 0, color: [0,0,0] }, 	// black
		{nr: 1, color: [255,255,255] }, // white
		{nr: 2, color: [255,0,0] }, 	// red
		{nr: 3, color: [0,255,0] }, 	// green
		{nr: 4, color: [0,0,255] }, 	// blue
		{nr: 5, color: [0,255,255] }, 	// light blue
		{nr: 6, color: [255,255,0] }, 	// yellow
		{nr: 7, color: [255,0,255] },  	// purple
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
			{ x: 1,	y: 0 },
			{ x: 0,	y: 1 },
			{ x: -1, y: 1 }
		    ]
		}, { color: 4, coordinates:
		    [
			{ x: 0, y: 0 },
			{ x: -1, y: 0 },
			{ x: 0,	y: 1 },
			{ x: 1,	y: 1 }
             	    ]
		}, { color: 5, coordinates:
		    [
			{ x: 0, y: 0 },
			{ x: 0,	y: 1 },
			{ x: 1,	y: 0 },
			{ x: 1,	y: 1 }
		    ]
		}, { color: 6, coordinates:
		    [
			{ x: 0,	y: -1 },		
			{ x: 0,	y: 0 },
			{ x: 0,	y: 1 },
			{ x: 0,	y: 2 }
		    ]
	        }, { color: 7, coordinates: 
		    [
			{ x: 0,	y: -1 },			
			{ x: 0,	y: 0 },
			{ x: -1, y: 0 },
			{ x: 1,	y: 0 }
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
	return this.color;
    };
	
    return that;
}

function init() {
    stage = new createjs.Stage("TetrisCanvas");
    createjs.Ticker.on("tick", tick);    
    createjs.Ticker.setFPS(30);
    
    startGame()
}

var block;
function startGame() {
    block = Block(newBlock())
    block.create(5, 1)
    block.addToStage()
}

function tick(event) {
    block.moveDown()
    stage.update(event);
}
