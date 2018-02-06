from random import uniform, choice
from math import floor, pow
import pickle
import os

class Gene():
    def __init__(self,  
                 rows_complete = uniform(-0.5, 0.5), 
                 weighted_height = uniform(-0.5, 0.5), 
                 cumulative_heights = uniform(-0.5, 0.5), 
                 relative_height = uniform(-0.5, 0.5), 
                 holes = uniform(0, 0.5), 
                 roughness = uniform(-0.5, 0.5),
                 fitness = -1):

        
        self.rows_complete      = rows_complete
        self.weighted_height    = weighted_height
        self.cumulative_heights =  cumulative_heights
        self.relative_height    = relative_height
        self.holes              = holes
        self.roughness          = roughness
        self.fitness            = fitness

class GeneticAI():
    def __init__(self, model_path):
        self.mutation_rate = 0.2
        self.mutation_step = 0.2
        self.archive = []
        self.genes = []
        self.population_size = 10
        self.current_gene = -1
        self.current_board = None
        self.current_shape = None
        self.next_shape = None
        self.model_path = model_path

        self.initial_population()

    def initial_population(self):
        self.read_dataset()
        self.evaluate_next_gene()

    def evaluate_next_gene(self):
        self.current_gene += 1
        if self.current_gene == len(self.genes):
            self.evolve()

    def update(self, fail, score):
        if fail:
            score -= 5000
       
        self.genes[self.current_gene].fitness = score
        self.evaluate_next_gene()

    def evolve(self):
        self.current_gene = 0
        self.genes = sorted(self.genes, key = lambda x: -x.fitness)
        self.archive += [self.genes[0].fitness]
        while len(self.genes) > self.population_size // 2:
            self.genes.pop()
        total_fitness = sum(gen.fitness for gen in self.genes)
        def random_gene():
            return self.genes[self.random_weighted_number(0, len(self.genes) - 1)]
        children = [self.genes[0]]
        while len(children) < self.population_size:
            children += [self.make_child(random_gene(), random_gene())]
        self.genes = children
    
    def make_child(self, mum, dad):
        child = Gene(
                        rows_complete = choice([mum.rows_complete, dad.rows_complete]),
                        weighted_height = choice([mum.weighted_height, dad.weighted_height]),
                        cumulative_heights = choice([mum.cumulative_heights, dad.cumulative_heights]),
                        relative_height = choice([mum.relative_height, dad.relative_height]),
                        holes = choice([mum.holes, dad.holes]),
                        roughness = choice([mum.roughness, dad.roughness])
                        )
        if uniform(0, 1) < self.mutation_rate:
            child.rows_complete += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.weighted_height += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.cumulative_heights += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.relative_height += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.holes += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.roughness += uniform(0, 1) *  self.mutation_step * 2 - self.mutation_step
        return child
    

    def next_move(self, gene_idx = -1):
        if gene_idx == -1:
            gene_idx = self.current_gene
        current_possible_moves = self.all_possible_move(self.current_board, self.current_shape, gene_idx)
        for move in current_possible_moves:
            rotation = move['rotate']
            shape = self.current_shape
            for _ in range(rotation):
                shape = self.rotate(shape)
            offx = move['offx']
            level = self.drop(self.current_board, shape, (offx, 0))
            board = self.place_shape(self.current_board, shape, (level,offx))
            move['rating'] += max(self.all_possible_move(board, self.next_shape, gene_idx), key = lambda x:x['rating'])['rating']
        best_choice = max(current_possible_moves, key=lambda x: x['rating'])
        
        return best_choice


    def all_possible_move(self, board, shape, gene_idx):
        possible_moves = []
        for rotation in range(4):
            for offx in range(len(board[0]) - len(shape[0]) + 1):
                level = self.drop(board, shape, (offx, 0))
                status = self.board_status(self.place_shape(board, shape, (level, offx)))
                rate = status['rows_complete'] * self.genes[gene_idx].rows_complete +\
                       status['weighted_height'] * self.genes[gene_idx].weighted_height +\
                       status['cumulative_heights'] * self.genes[gene_idx].cumulative_heights +\
                       status['relative_height'] * self.genes[gene_idx].relative_height +\
                       status['holes'] * self.genes[gene_idx].holes +\
                       status['roughness'] * self.genes[gene_idx].roughness
                possible_moves += [{'rotate':rotation, 'offx':offx, 'rating':rate, 'status':status}]
            shape = self.rotate(shape)
        
        return possible_moves
        
    def drop(self, board, shape, offset):
        off_x, off_y = offset
        last_level = len(board) - len(shape) + 1
        for level in range(off_y, last_level):
            for i in range(len(shape)):
                for j in range(len(shape[0])):
                    if board[level+i][off_x+j] == 1 and shape[i][j] == 1:
                        return level - 1
        return last_level - 1

    def place_shape(self, board, shape, pos):
        board_ = [row[:] for row in board]
        level, offx = pos
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 1:
                    board_[level+i][offx+j] = shape[i][j]
        return board_

    def rotate(self, shape):
        return [row[::-1] for row in zip(*shape)]

    def board_status(self, board):
        status = {'rows_complete' : 0,
                  'weighted_height':0,
                  'cumulative_heights':0,
                  'relative_height':0,
                  'holes':0,
                  'roughness':0
                 }
        def get_completed_line():
            complete_line = 0
            for i, line in enumerate(board):
                if line.count(0) == 0:
                    del board[i]
                    board.insert(0, [0 for _ in range(len(board[0]))])
                    complete_line += 1
            return complete_line

        def get_holes_and_peaks():
            rotate_board = [row for row in zip(*board)]
            holes = 0
            peaks = [0 for _ in range(len(rotate_board))]
            
            for idx, row in enumerate(rotate_board):
                if row.count(1) > 0:
                    holes += len(row) - row.index(1) - sum(row)
                    peaks[idx] = len(row) - row.index(1)
            return holes, peaks

        status['rows_complete'] = get_completed_line()
        holes, peaks = get_holes_and_peaks()
        status['holes'] = holes
        status['weighted_height'] = pow(max(peaks), 1.5)
        status['cumulative_heights'] = sum(peaks)
        status['relative_height'] = max(peaks) - min(peaks)
        status['roughness'] = sum(abs(peaks[i] - peaks[i+1]) for i in range(len(peaks) - 1))
        return status

    def random_weighted_number(self, min_, max_):
        return floor(pow(uniform(0,1), 2) * (max_ - min_ + 1) + min_)

    def save_dataset(self):
        with open(self.model_path, 'wb+') as f:
            pickle.dump((self.genes, self.archive, self.current_gene), f, -1)
            

    def read_dataset(self):
        if not os.path.isfile(self.model_path):
            self.genes = [Gene() for _ in range(self.population_size)]
        else:
            with open(self.model_path, 'rb') as f:
                self.genes, self.archive, self.current_gene = pickle.load(f)



            
