import re
import CEC2022
import numpy as np


def read_x(num_sampling, num_x):
    X = []
    m = num_x+1
    # f = open("/data/s3202844/data/samplingX.txt", "r")
    # f = open("/data/s3202844/data/samplingX_002D.txt", "r")
    f = open("config/samplingX_010D.txt", "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        x = []
        content = lines[m*i:m*i+m]
        for j in range(1, m):
            temp = []
            line = re.split(r"[ ]+", content[j][:-1])
            for n in line[1:]:
                temp += [float(n)]
            x += [temp]
        X += [x]
    return np.array(X)


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


def save_origin(problem, x):
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: None.")
    results = []
    for i in range(x.shape[0]):
        problem.values(x[i].T)
        results += [problem.ObjFunc.tolist()]
    results = np.array(results)
    np.savetxt(f"ecta2024_data/origin/{problem.func}_0.000000.txt", results)


def x_rotation(problem, matrix, x):
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: x rotation.")
    for matrix_id in range(matrix.shape[0]):
        results = []
        for i in range(x.shape[0]):
            tempx = x[i].T.copy()
            for j in range(tempx.shape[1]):
                tempx[:, j] = np.dot(matrix[matrix_id], tempx[:, j])
            problem.values(tempx)
            results += [problem.ObjFunc.tolist()]
        results = np.array(results)
        file_name = f"ecta2024_data/x_rotation/{pid}_{matrix_id}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, results)


def x_scaling(problem, x):
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: x scaling.")
    for log_k in range(-30, 31, 1):
        results = []
        if log_k == 0:
            continue
        k = 2**(log_k/10.0)
        kx = x.copy() * k
        for i in range(x.shape[0]):
            input_x = kx[i].T.copy()
            problem.values(input_x)
            results += [problem.ObjFunc.tolist()]
        results = np.array(results)
        file_name = f"ecta2024_data/x_scaling/{pid}_{log_k/10:.6f}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, results)


def transformations(problem_id, x):
    rvec_file_path = "config/random_look_10d_rotation_matrices.txt"
    array = read_matrices_to_array(rvec_file_path)
    problem = CEC2022.cec2022_func(problem_id)
    # save_origin(problem, x)
    # x_rotation(problem, array, x)
    x_scaling(problem, x)


if __name__ == "__main__":
    x = read_x(100, 1000)
    for problem_id in range(6, 13):
        transformations(problem_id, x)
