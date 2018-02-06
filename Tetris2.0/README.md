# HOW I DID THIS TETRIS AI

## 1.0 Genetic Algorithm

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


#### Rules:

* This tetris board with dimensions 14 * 25(so weird I know :p but don't matter right?)
* we measure the algorithm or performance of gene by score it get in game
* if "game over" will minus extra scores
* clean multiple lines once, will get extra scores

### Implementation and Results

The following table show the improvement in score (heighter score better) over first 250 games:

<table>
  <thead>
    <tr>
      <th>Game</th>
      <th>Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>1</td>
      <td>14</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>50</td>
      <td>20</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>50</td>
      <td>20</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>100</td>
      <td>15</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>150</td>
      <td>31</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>200</td>
      <td>53182</td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>250</td>
      <td>2655461</td>
    </tr>
  </tbody>
</table>

after about 264 times train, using "game over" to finish once training cost much more time, and after more, tetris AIPlayer works like "keep alive", but for most time it only clean one line once, and left lots holes inside

### Attempted Learning Enhancements

So to improve from this, we try to train it by "limit" pieces and wish it learn/get the last rule - "clean multiple lines once, will get extra scores", in the beginning we set 100 pieces once, it seems work, more time ai can clean "2 lines" once even "3 lines", and holes to be fewer, but the weight of "weighted_height" become larger, that means, ai prefer to put pieces on single column, and the peek get much higer

### TODO

So far there are still many things need to be done to impove this tetris aiplayer

- [ ] estimate the algorithm, I am not sure the "keep alive" and "clean more lines once" with is better. Or should we use human instance to train AI(maybe not).
- [ ] except genetic algorithm, can I use or combine other algorithm to impove the performance
- [ ] another is the front end thing, it still rough haha

## 2.0 Reinforcement Learning

### Implementation and Results
### Attempted Learning Enhancements

