# Sudoku Background
# Sudoku is a game played on a 9x9 grid. The goal of the game is to fill all cells of the grid with digits from 1 to 9,
# so that each column, each row, and each of the nine 3x3 sub-grids (also known as blocks) contain all of the digits
# from 1 to 9.
#
# Sudoku Solution Validator
# Write a function validSolution/ValidateSolution/valid_solution() that accepts a 2D array representing a Sudoku board,
# and returns true if it is a valid solution, or false otherwise. The cells of the sudoku board may also contain 0's,
# which will represent empty cells. Boards containing one or more zeroes are considered to be invalid solutions.
# The board is always 9 cells by 9 cells, and every cell only contains integers from 0 to 9.
# Examples
# validSolution([
#   [5, 3, 4, 6, 7, 8, 9, 1, 2],
#   [6, 7, 2, 1, 9, 5, 3, 4, 8],
#   [1, 9, 8, 3, 4, 2, 5, 6, 7],
#   [8, 5, 9, 7, 6, 1, 4, 2, 3],
#   [4, 2, 6, 8, 5, 3, 7, 9, 1],
#   [7, 1, 3, 9, 2, 4, 8, 5, 6],
#   [9, 6, 1, 5, 3, 7, 2, 8, 4],
#   [2, 8, 7, 4, 1, 9, 6, 3, 5],
#   [3, 4, 5, 2, 8, 6, 1, 7, 9]
# ]); // => true

import numpy as np


testData = [[5, 3, 4, 6, 7, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 0, 3, 4, 9],
            [1, 0, 0, 3, 4, 2, 5, 6, 0],
            [8, 5, 9, 7, 6, 1, 0, 2, 0],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 0, 1, 5, 3, 7, 2, 1, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 0, 0, 4, 8, 1, 1, 7, 9]]


def valid_solution(board):
    counter = 0
    testList = []
    testMiniMatrixList = []
    for i in board:
        if counter < 9:
            testMiniMatrixList.append(i[:3])
            testMiniMatrixList.append(i[3:6])
            testMiniMatrixList.append(i[6:])
            counter += 1
    Temporary = []
    counter = 0
    while counter < 26:
        for j in range(3):
            for i in range(0 + counter, 7 + counter, 3):
                Temporary = Temporary + testMiniMatrixList[i]
            testList.append(Temporary)
            Temporary = []
            counter += 1
        counter += 6
    for i in board:
        testList.append(i)
    for i in np.transpose(board):
        testList.append(i)
    for i in testList:
        if len(set(i)) != 9 or sum(set(i)) != 45:
            return False
    return True


print(valid_solution(testData))