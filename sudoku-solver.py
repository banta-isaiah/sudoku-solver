import math
from collections import defaultdict
import itertools 
import prettytable


class sudoku:
    '''

    '''
    def __init__(self, clues = []):
        
        self.clue_counter = 0
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
        self.clues = clues
        if self.clues != []:
            for clue in self.clues:
                self.puzzle[clue[0]][clue[1]] = clue[2]
                self.clue_counter += 1
        
    
    def add_clues(self, new_clues):
        for clue in new_clues:
            self.puzzle[clue[0]][clue[1]] = clue[2]
            self.clue_counter += 1
        return
    

    def _print(self):
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
        return

    def solution(self, solutions):
        for key,value in solutions.items():
            self.puzzle[key[0]][key[1]] = str(value)
        return


    
class solver:
    
    def __init__(self,puzzle):
        '''
        '''
        self.domain_list = list('123456789')
        self.variable_list = [(x,y) for x in range(9) for y in range(9)]
        self.neighbor_list = []
        self.neighbors = defaultdict(list)  
        self.givens = {}

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

        self.bf_count = 0
        self.bt_count = 0
        
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.givens[(i,j)] = str(puzzle[i][j])



    def is_solution(self, assignment):
        '''Checks whether a given assignment is actually a solution.
        '''
        for pair in self.neighbor_list:
            if (assignment[pair[0]]) == (assignment[pair[1]]):
                return False
        return True

    def select_unassigned_variable(self, assignment, domains = None):
        '''Selects a variable that has not yet been given a value according to
        the given assignment.
        Currently this just selects the first variable in variable_list that
        has not yet been given a value in the assignment. 
        Large increases in efficiency are possible with some more intelligent 
        selection criteria, but it isn't necessary to do this for the 
        map-coloring problem.
        '''
        if domains == None:
            for var in self.variable_list:
                if var not in assignment:
                    return var
        return None

    def solve_backtrack_search(self):
        '''A helper function that sets up our domains and initial assignment, then 
        calls a recursive backtracking search that will do the hard work.
        
        You should not need to change this function.
        '''
        domains = {}
        assignment = self.givens
        for var in self.variable_list:  
            domains[var] = self.domain_list[:]   
        for key,value in self.givens.items():
            domains[key] = [value]
        result = self.backtrack(assignment, domains)
        if self.is_solution(result):
            return result
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
    # Create a sudoku puzzle with clues
    puzzle1 = sudoku([(0,0,5)])
    # We can add more clues 
    puzzle1.add_clues([(0,1,7),(5,8,1)])
    # Print out unsolved puzzle with updated clues
    puzzle1._print()
    
    # We pass a puzzle to our solver
    test0 = solver(puzzle1.puzzle)

    # Updating our puzzle with the solved values and printing the result
    puzzle1.solution(test0.solve_backtrack_search())
    puzzle1._print()

    #Stats
    table0 = prettytable.PrettyTable(["Sudoku Puzzle 1", '-'])
    #table0.add_row(['time'])
    table0.add_row(['clues',puzzle1.clue_counter])
    table0.add_row(['backtracks',test0.bt_count])
    print(table0)
main()

