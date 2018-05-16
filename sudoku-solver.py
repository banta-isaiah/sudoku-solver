import math
from collections import defaultdict
import itertools 
from prettytable import PrettyTable
import time
import random

    
class sudoku_solver:
    '''
    '''
    def __init__(self,puzzle_file = None): 

        # Initialized Stats
        self.bt_count = 0
        self.time_elapsed = 0
        self.clue_counter = 0

        # Create table
        self.stats_table = PrettyTable()
        self.stats_table.field_names = ["time", "clues", "backtracks"]

        self.puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       ]

        # Setting up necessary variables
        self.domain_list = list('123456789')
        self.variable_list = [(x,y) for x in range(9) for y in range(9)]
        self.neighbor_list = []
        self.neighbors = defaultdict(list) 
        self.givens = {}

        # Grab sudoku puzzle from file
        file = open(puzzle_file)
        clues = file.read().splitlines()
        row = 0
        col = 0
        for clue in clues:
            clue_row = list(clue)
            for cell in clue_row:
                self.puzzle[row][col] = int(cell)
                if(int(cell)):
                    self.givens[(row,col)] = int(cell)
                    self.clue_counter += 1
                col += 1
                col = col % 9
            row += 1
            row = row % 9

        # This is the same for all standard sudoku puzzles.
        for i in range(9):
            for j in range(9):
                for k in range(8):
                    # Cells in a row are neighbors of each other
                    self.neighbors[(i,j)].append((i,(k+j+1)%9))

                    # Cells in a column are neighbors of each other
                    self.neighbors[(i,j)].append(((k+i+1)%9,j))

                    # Insert into Neighbor List
                    self.neighbor_list.append(((i,j),(i,(k+j+1)%9)))
                    self.neighbor_list.append(((i,j),((k+i+1)%9,j)))
                    
                for k in range(9):
                    # Cells in the same box are neighbors of each other
                    a = k//3+i//3*3
                    b = k%3+j//3*3
                    if (i,j) != (a,b):
                        self.neighbors[(i,j)].append((a,b))

                        # Insert into Neighbor List
                        self.neighbor_list.append(((i,j),(a,b)))


    def _print(self,stats=False):
            print('=========================')
            counter1 = 0
            counter2 = 0
            row = ''
            for i in range(len(self.puzzle)):
                counter1 += 1
                row += "| "
                for j in range(len(self.puzzle[i])):
                    counter2 += 1
                    if self.puzzle[i][j]:
                        row += str(self.puzzle[i][j]) + " "
                    else:
                        row += '. '
                    if (counter2 % 3) == 0:
                        row += "| "
                print(row)
                row = '' 
                if (counter1 % 3 == 0) and (counter1 != 9):
                    print('|-------+-------+-------|')
            print('=========================')

            if stats == True:
               print(self.stats_table)
            return

    def add_clues(self, new_clues):
            for clue in new_clues:
                self.puzzle[clue[0]][clue[1]] = clue[2]
                self.clue_counter += 1
            return 

    def solution(self, solutions):
        for key,value in solutions.items():
            self.puzzle[key[0]][key[1]] = str(value)
        return

    def is_solution(self, assignment):
        '''Varifies solution.
        '''
        for pair in self.neighbor_list:
            if (assignment[pair[0]]) == (assignment[pair[1]]):
                return False
        return True

    def select_unassigned_variable(self, assignment, domains = None):
        '''Selects a variable that has not yet been given a value according to
        the given assignment. Selects first variable in self.variable_list.
        '''
        if domains == None:
            for var in self.variable_list:
                if var not in assignment:
                    return var
        return None

    def solve(self):
        '''A helper function that sets up our domains and initial assignment, then 
        calls a recursive backtracking search that will do the hard work.
        '''
        print("Our unsolved puzzle:")
        self._print()
        domains = {}
        assignment = self.givens
        for var in self.variable_list:  
            domains[var] = self.domain_list[:]   
        # Update domains with given clues
        for key,value in self.givens.items():
            domains[key] = [value]
        # Time our backtracking, AC-3 algorithm
        start = time.clock()
        print('Solving...')
        result = self.backtrack(assignment, domains)
        end = time.clock()
        self.time_elapsed = round(end - start, 2)
        # If our solution is satisfiable, the print out the puzzle and stats
        if self.is_solution(result):
            self.solution(result)
            self.stats_table.add_row([str(self.time_elapsed) + 's',self.clue_counter,self.bt_count])
            self._print(True)
            return 
        else:
            return "Error! Backtrack returned an assignment that is not a solution"

    def backtrack(self, assignment, domains): 
        if len(assignment) == len(domains):
            return assignment
        var = self.select_unassigned_variable(assignment)   
        for val in domains[var]:
            assignment[var] = val   
            saved = domains[var]
            domains[var] = [val]
            inferences = self.ac3(domains)  
            if inferences != False:
                self.bt_count += 1
                result = self.backtrack(assignment, domains)
                if result != False:
                    return result
            del assignment[var] 
            if inferences != False:
                for key, values in inferences.items():
                    domains[key].extend(values)
            domains[var] = saved 
        return False
         
    def ac3(self, domains):
        q = self.neighbor_list  
        for pair in q:
            q = q + [(pair[1], pair[0])]
        removeddict = {x:[] for x in domains}        
        while len(q) > 0:
            (xi, xj) = q.pop() 
            removedlist = self.revise(xi, xj, domains)
            if len(removedlist) > 0:
                if len(domains[xi]) == 0:
                    if removeddict != False:
                        for key, values in removeddict.items():
                            domains[key].extend(values)
                        domains[xi].extend(removedlist)
                    return False
                for xk in self.neighbors[xi]:      
                    if xk != xj:
                        q.append((xk, xi))
            removeddict[xi].extend(removedlist)
        return removeddict
     
    def revise(self, xi, xj, domains):
        removedlist = []
        for valx in domains[xi]:
            cansatisfy = False
            for valy in domains[xj]:
                if valx != valy:
                    cansatisfy = True
            if cansatisfy == False:
                removedlist.append(valx)
        for val in removedlist:
            domains[xi].remove(val)
        return removedlist


def main():
    test0 = sudoku_solver('sudoku.txt')
    test0.solve()

main()

