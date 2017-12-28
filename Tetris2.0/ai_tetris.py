from random import uniform, choice
from math import floor, pow
import pickle

class Genome():
    def __init__(self, id_ = uniform(0, 1), 
                       rows_complete = uniform(-0.5, 0.5), 
                       weighted_height = uniform(-0.5, 0.5), 
                       cumulative_heights = uniform(-0.5, 0.5), 
                       relative_height = uniform(-0.5, 0.5), 
                       holes = uniform(0, 0.5), 
                       roughness = uniform(-0.5, 0.5),
                       fitness = -1):

        self.id_                = id_
        self.rows_complete      = rows_complete
        self.weighted_height    = weighted_height
        self.cumulative_heights =  cumulative_heights
        self.relative_height    = relative_height
        self.holes              = holes
        self.roughness          = roughness
        self.fitness            = fitness

class AIPlayer():
    def __init__(self):
        self.mutation_rate = 0.05
        self.mutation_step = 0.2
        self.archive = []
        self.genomes = []
        self.population_size = 50
        self.generation = 0
        self.current_genome = -1
        self.current_board = None
        self.current_shape = None

        self.initial_population()

    def initial_population(self):
        self.genomes =[Genome() for _ in range(self.population_size)]
        self.evaluate_next_genome()

    def evaluate_next_genome(self):
        self.current_genome += 1
        if self.current_genome == len(self.genomes):
            self.evolve()

    def update(self, fail, score):
        if fail:
            self.genomes[self.current_genome].fitness = score - 500
            self.evaluate_next_genome()
            return
        return self.next_move()

    def evolve(self):
        self.current_genome = 0
        self.generation += 1
        self.genomes = sorted(self.genomes, key = lambda x: -x.fitness)
        self.archive += [self.genomes[0]]
        while len(self.genomes) > self.population_size // 2:
            self.genomes.pop()
        total_fitness = sum(gen.fitness for gen in self.genomes)
        def random_genome():
            return self.genomes[self.random_weighted_number(0, len(self.genomes) - 1)]
        children = [self.genomes[0]]
        while len(children) < self.population_size:
            children += [self.make_child(random_genome(), random_genome())]
        self.genomes = children
    
    def make_child(self, mum, dad):
        child = Genome(id_ = uniform(0, 1),
                        rows_complete = choice([mum.rows_complete, dad.rows_complete]),
                        weighted_height = choice([mum.weighted_height, dad.weighted_height]),
                        cumulative_heights = choice([mum.cumulative_heights, dad.cumulative_heights]),
                        relative_height = choice([mum.relative_height, dad.relative_height]),
                        holes = choice([mum.holes, dad.holes]),
                        roughness = choice([mum.roughness, dad.roughness]))
        if uniform(0, 1) < self.mutation_rate:
            child.rows_complete += uniform(0, 1) *  mutation_step * 2 - mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.weighted_height += uniform(0, 1) *  mutation_step * 2 - mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.cumulative_heights += uniform(0, 1) *  mutation_step * 2 - mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.relative_height += uniform(0, 1) *  mutation_step * 2 - mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.holes += uniform(0, 1) *  mutation_step * 2 - mutation_step
        if uniform(0, 1) < self.mutation_rate:
            child.roughness += uniform(0, 1) *  mutation_step * 2 - mutation_step
        return child
    

    def next_move(self):
        best_choice = max(self.all_possible_move(), key = lambda x: x['rating'])
        #print(best_choice['rating'])
        return best_choice

    def all_possible_move(self):
        possible_moves = []
        for rotation in range(4):
            for offx in range(len(self.current_board[0]) - len(self.current_shape[0]) + 1):
                level = self.drop((offx, 0))
                status = self.board_status(self.place_shape((level, offx)))
                rate = status['rows_complete'] * self.genomes[self.current_genome].rows_complete +\
                       status['weighted_height'] * self.genomes[self.current_genome].weighted_height +\
                       status['cumulative_heights'] * self.genomes[self.current_genome].cumulative_heights +\
                       status['relative_height'] * self.genomes[self.current_genome].relative_height +\
                       status['holes'] * self.genomes[self.current_genome].holes +\
                       status['roughness'] * self.genomes[self.current_genome].roughness
                possible_moves += [{'rotate':rotation, 'offx':offx, 'rating':rate, 'status':status}]
            self.rotate()
        
        return possible_moves
        
    def drop(self, offset):
        off_x, off_y = offset
        last_level = len(self.current_board) - len(self.current_shape) + 1
        for level in range(off_y, last_level):
            for i in range(len(self.current_shape)):
                for j in range(len(self.current_shape[0])):
                    if self.current_board[level+i][off_x+j] == 1 and self.current_shape[i][j] == 1:
                        return level - 1
        return last_level - 1

    def place_shape(self,pos):
        board_ = [row[:] for row in self.current_board]
        level, offx = pos
        for i in range(len(self.current_shape)):
            for j in range(len(self.current_shape[0])):
                if self.current_shape[i][j] == 1:
                    board_[level+i][offx+j] = self.current_shape[i][j]
        return board_

    def rotate(self):
        self.current_shape = [row[::-1] for row in zip(*self.current_shape)]

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


    #TODO: read and save dataser, not correct yet
    def save_dataset(self):
        with open('genome', 'wb+') as f:
            f.write(b'')

        with open('genome', 'ab') as f:
            for genome in self.genomes:
                pickle.dump(genome, f, -1)

        with open('archive', 'ab+') as f:
            for genome in self.archive:
                pickle.dump(genome, f, -1)
            self.archive = []

    def read_dataset(self):
        with open('genome', 'rb') as f:
            data = pickle.load(f)
            with open('genome.txt', 'w+') as g:
                g.write(data.fitness)




