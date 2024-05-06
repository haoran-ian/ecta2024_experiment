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


def trace(matrix):
    return np.trace(matrix)


filename = "config/random_look_10d_rotation_matrices.txt"
array = read_matrices_to_array(filename)
flag = True
for i in range(array.shape[0]):
    ind = int(i/5)
    low = ind*0.2-2.
    high = (ind+1)*0.2-2.
    t = trace(array[i])
    if t < low or t > high:
        flag = False
        print(f"Trace of matrix {i} is {t}, which is not in the range [{low}, {high}]")
if flag:
    print("All traces are in the correct range")