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

def save_origin(problem, x):
    print(f"Processing: problem id: {problem.func}, transformation: None.")
    results = []
    for i in range(x.shape[0]):
        problem.values(x[i].T)
        results += [problem.ObjFunc.tolist()]
    results = np.array(results)
    np.savetxt(f"ecta2024_data/origin/{problem.func}_0.000000.txt", results)

def transformations(problem_id, x):
    problem = CEC2022.cec2022_func(problem_id)
    # problem.values(np.array([[0.] for _ in range(10)]))
    # print(problem.ObjFunc)
    save_origin(problem, x)

if __name__ == "__main__":
    x = read_x(100, 1000)
    for problem_id in range(6, 13):
        transformations(problem_id, x)