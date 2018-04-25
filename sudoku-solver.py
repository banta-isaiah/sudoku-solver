import math


class sudoku_solver:

    def __init__(self, clues = []):
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
        if clues != []:
            for clue in self.clues:
                self.puzzle[clue[0]][clue[1]] = clue[2]
        
    
    def add_clues(self, new_clues):
        for clue in new_clues:
            self.puzzle[clue[0]][clue[1]] = clue[2]
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
                    row += str('. ')
                if (counter2 % 3) == 0:
                    row += "| "
            print(row)
            row = ''
            if (counter1 % 3 == 0) and (counter1 != 9):
                print('--------+-------+--------')
        print('=========================')
        return

    


def main():
    puzzle1 = sudoku_solver([(1,2,3)])
    puzzle1._print()
    puzzle1.add_clues([(1,3,4),(2,4,3),(4,5,6)])
    puzzle1._print()
main()
