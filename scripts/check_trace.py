import numpy as np


def read_matrices_to_array(filename):
    with open(filename, 'r') as file:
        data = []
        for line in file:
            if line[0] == "#" or line[0] == "B" or line == "\n":
                continue
            row = list(map(float, line.split()))
            if len(row) == 10:
                data.append(row)
    data = np.array(data)
    if data.shape[0] >= 1000:
        return data[:1000].reshape((100, 10, 10))
    else:
        raise ValueError("Not enough data to form a (100, 10, 10) array")


def is_orthogonal(matrix):
    if matrix.shape != (10, 10):
        return False
    identity = np.eye(10)
    matrix_transposed = matrix.T
    product1 = np.dot(matrix, matrix_transposed)
    product2 = np.dot(matrix_transposed, matrix)
    return np.allclose(product1, identity) and np.allclose(product2, identity)


filename = "config/random_look_10d_rotation_matrices.txt"
array = read_matrices_to_array(filename)
trace_flag = True
orthogonal_flag = True
for i in range(array.shape[0]):
    ind = int(i/5)
    low = ind*0.2-2.
    high = (ind+1)*0.2-2.
    t = np.trace(array[i])
    if t < low or t > high:
        trace_flag = False
        print(
            f"Trace of matrix {i} is {t}, which is not in the range [{low}, {high}]")
    if not is_orthogonal(array[i]):
        orthogonal_flag = False
        print(f"Matrix {i} is not orthogonal.")
if trace_flag:
    print("All traces are in the correct range.")
if orthogonal_flag:
    print("All traces are orthogonal.")
