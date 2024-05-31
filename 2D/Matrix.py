"""
works on matrices of the shape:
mat = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1]
]
"""

def rowSwap(mat, row_1, row_2):
    buffer = mat[row_1]
    mat[row_1] = mat[row_2]
    mat[row_2] = buffer

def rowMult(mat, target_row, add_row, mult):
    for i in range(len( mat[target_row] )):
        mat[target_row][i] += mat[add_row][i] * mult

def rowScale(mat, row, mult):
    for i in range(len(mat[row])):
        mat[row][i] *= mult