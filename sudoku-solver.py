import math
from collections import defaultdict
import itertools 
import prettytable
import time

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

        # Insert clues into puzzle 
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    self.givens[(i,j)] = str(puzzle[i][j])

        # Stats
        self.bf_count = 0
        self.bt_count = 0

        self.time_elapsed = 0

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
        # Update domains with given clues
        for key,value in self.givens.items():
            domains[key] = [value]
        # Time our backtracking, AC-3 algorithm
        start = time.clock()
        result = self.backtrack(assignment, domains)
        end = time.clock()
        self.time_elapsed = round(end - start, 2)
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
    print('-----~`PUZZLE 0`~-----\n') 
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
    table0 = prettytable.PrettyTable(["Sudoku Puzzle 0", '-'])
    table0.add_row(['time', str(test0.time_elapsed) + 's'])
    table0.add_row(['clues',puzzle1.clue_counter])
    table0.add_row(['backtracks',test0.bt_count])
    print(table0) 
    
    print('-----~`PUZZLE 1`~-----\n') 
    # Puzzle with _Easy_ difficulty
    easypuz = sudoku([(0,2,4),(0,3,6),(0,4,8),(0,5,1),(0,8,9),
                      (1,1,1),(1,2,6),(1,6,3),(1,7,7),(1,8,4),
                      (2,1,2),(2,2,9),(2,3,7),(2,5,3),
                      (3,0,1),(3,2,3),
                      (4,1,4),(4,3,2),(4,5,5),(4,7,1),
                      (5,6,5),(5,8,8),
                      (6,3,5),(6,5,9),(6,6,1),(6,7,3,),
                      (7,0,7),(7,1,9),(7,6,4),(7,7,8),
                      (8,0,6),(8,3,4),(8,4,1),(8,5,8),(8,6,9)])
    easypuz._print()

    easypuz_solve = solver(easypuz.puzzle)
    easypuz.solution(easypuz_solve.solve_backtrack_search())

    easypuz._print()

    table1 = prettytable.PrettyTable(["Sudoku Puzzle 1", '-'])
    table1.add_row(['time', str(easypuz_solve.time_elapsed) + 's'])
    table1.add_row(['clues',easypuz.clue_counter])
    table1.add_row(['backtracks',easypuz_solve.bt_count])
    table1.add_row(['difficulty', 'easy'])
    print(table1)

    print('-----~`PUZZLE 2`~-----\n')
    # Puzzle with _Medium_ difficulty
    medpuz = sudoku([(0,4,2),(0,7,4),
                     (1,2,8),(1,5,7),
                     (2,0,1),(2,2,4),(2,3,8),(2,6,6),(2,7,3),
                     (3,0,7),(3,3,6),(3,7,2),(3,8,8),
                     (4,2,9),(4,4,3),(4,6,7),
                     (5,0,2),(5,1,4),
                     (6,1,6),(6,2,2),(6,5,3),(6,6,9),(6,8,4),
                     (7,3,7),(7,6,5),
                     (8,1,3),(8,4,5)])
    medpuz._print()

    medpuz_solve = solver(medpuz.puzzle)
    medpuz.solution(medpuz_solve.solve_backtrack_search())

    medpuz._print()

    table2 = prettytable.PrettyTable(["Sudoku Puzzle 2", '-'])
    table2.add_row(['time', str(medpuz_solve.time_elapsed) + 's'])
    table2.add_row(['clues',medpuz.clue_counter])
    table2.add_row(['backtracks',medpuz_solve.bt_count])
    table2.add_row(['difficulty', 'medium'])
    print(table2)

    # Puzzle with _Hard_ difficulty
    print('-----~`PUZZLE 3`~-----\n')
    # Puzzle with _Medium_ difficulty
    hardpuz = sudoku([(0,0,7),(0,1,3),(0,2,4),(0,4,2),(0,8,9),
                      (1,0,1),(1,5,7),
                      (2,5,5),(2,6,7),(2,7,6),
                      (3,7,9),(3,8,7),
                      (4,1,2),(4,4,4),(4,7,1),
                      (5,0,6),(5,1,8),
                      (6,1,5),(6,2,2),(6,3,6),
                      (7,3,2),(7,8,6),
                      (8,0,9),(8,4,5),(8,6,2),(8,7,8),(8,8,4)])
    hardpuz._print()

    hardpuz_solve = solver(hardpuz.puzzle)
    hardpuz.solution(hardpuz_solve.solve_backtrack_search())

    hardpuz._print()

    table3 = prettytable.PrettyTable(["Sudoku Puzzle 3", '-'])
    table3.add_row(['time', str(hardpuz_solve.time_elapsed) + 's'])
    table3.add_row(['clues',hardpuz.clue_counter])
    table3.add_row(['backtracks',hardpuz_solve.bt_count])
    table3.add_row(['difficulty', 'hard'])
    print(table3)

    # Puzzle with _Very Hard_ dificulty
    print('-----~`PUZZLE 4`~-----\n')
    # Puzzle with _Medium_ difficulty
    veryhardpuz = sudoku([(0,3,9),(0,6,4),(0,7,6),
                          (1,4,5),(1,5,8),(1,6,7),
                          (2,3,1),(2,4,7),(2,7,5),
                          (3,2,2),(3,4,9),(3,8,4),
                          (4,0,1),(4,8,8),
                          (5,0,5),(5,4,8),(5,6,2),
                          (6,1,2),(6,4,1),(6,5,9),
                          (7,2,5),(7,3,8),(7,4,2),
                          (8,1,3),(8,2,9),(8,5,5)])

    veryhardpuz._print()

    veryhardpuz_solve = solver(veryhardpuz.puzzle)
    veryhardpuz.solution(veryhardpuz_solve.solve_backtrack_search())

    veryhardpuz._print()

    table4 = prettytable.PrettyTable(["Sudoku Puzzle 4", '-'])
    table4.add_row(['time', str(veryhardpuz_solve.time_elapsed) + 's'])
    table4.add_row(['clues',veryhardpuz.clue_counter])
    table4.add_row(['backtracks',veryhardpuz_solve.bt_count])
    table4.add_row(['difficulty', 'very hard'])
    print(table4)

main()

