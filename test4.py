import numpy as np
matrix1 = input("Enter a matrix: ")
matrix2 = input("Enter a matrix")
matrix1 = np.matrix(matrix1)
matrix2 = np.matrix(matrix2)
result = matrix1 + matrix2
result.tolist()
print(result)