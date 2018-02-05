# HOW I DID THIS TETRIS AI

Genetic algorithm basic of this tetris AI

### Seven characteristic values(genes):

- rows_complete
- weighted_height
- cumulative_heights
- relative_height
- holes
- roughness
- fitness

for each piece, we choice the best position(rotate and offset) by the score it gets based on these characteristic values, plus the next piece's max score can get based on current piece's choice

for each 10th(or based on population_size value in AIPlayer) update, AI will evolve once

### How evolve works

we just keep the first half best performance(judged by the game score it geted) genes, and generate another half (of population size) genes by these first half genes. Child gene get random characteristic from parents and with mutation possible

### How it works/What else have we try

#### Rules:

* This tetris board with dimensions 14 * 25(so weird I know :p but don't matter right?)
* we measure the algorithm or performance of gene by score it get in game
* if "game over" will minus extra scores
* clean multiple lines once, will get extra scores


After the first about 3-4 hours train, tetris AIPlayer works like "keep alive", but for most time it only clean one line once, and left lots holes inside

So to improve from this, we try to train it by "limit" pieces and wish it learn/get the last rule - "clean multiple lines once, will get extra scores", in the beginning we set 100 pieces once, it seems work, more time ai can clean "2 lines" once even "3 lines", and holes to be fewer, but the weight of "weighted_height" become larger, that means, ai prefer to put pieces on single column, and the peek get much higer

### TODO

So far there are still many things need to be done to impove this tetris aiplayer

- [ ] estimate the algorithm, I am not sure the "keep alive" and "clean more lines once" with is better. Or should we use human instance to train AI(maybe not).
- [ ] except genetic algorithm, can I use or combine other algorithm to impove the performance
- [ ] another is the front end thing, it still rough haha