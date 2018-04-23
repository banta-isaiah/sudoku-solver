import math


class sudoku_solver:
    def __init__(self):
        self.puzzle = [[0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0,],
                       ]
    
    def clues(self):
        return 

    def _print(self):
        row = ''
        for i in range(len(self.puzzle)):
            for j in range(len(self.puzzle[i])):
                row += str(self.puzzle[i][j]) + " "
            print(row)
            row = ''
        return


def main():
    puzzle1 = sudoku_solver()
    puzzle1._print()
main()
