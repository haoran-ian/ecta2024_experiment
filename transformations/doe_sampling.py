import os
import CEC2022
import numpy as np
from doe2vec import doe_model


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
    if not os.path.exists("ecta2024_data/origin/doe"):
        os.makedirs("ecta2024_data/origin/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: None.")
    problem.values(x.T.copy())
    results = problem.ObjFunc
    np.savetxt(f"ecta2024_data/origin/doe/{pid}.txt", results)


def x_rotation(problem, matrix, x):
    if not os.path.exists("ecta2024_data/x_rotation/doe"):
        os.makedirs("ecta2024_data/x_rotation/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: x rotation.")
    for matrix_id in range(matrix.shape[0]):
        tempx = x.T.copy()
        for j in range(tempx.shape[1]):
            rvec = matrix[matrix_id].copy()
            tempx[:, j] = np.dot(rvec, tempx[:, j])
        problem.values(tempx)
        results = problem.ObjFunc
        file_name = f"ecta2024_data/x_rotation/doe/{pid}_{matrix_id}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, results)


def x_scaling(problem, x):
    if not os.path.exists("ecta2024_data/x_scaling/doe"):
        os.makedirs("ecta2024_data/x_scaling/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: x scaling.")
    for log_k in range(-30, 31, 1):
        if log_k == 0:
            continue
        k = 2**(log_k/10.0)
        kx = x.copy() * k
        input_x = kx.T.copy()
        problem.values(input_x)
        results = problem.ObjFunc
        file_name = f"ecta2024_data/x_scaling/doe/{pid}_{log_k/10:.6f}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, results)


def x_translation(problem, x):
    if not os.path.exists("ecta2024_data/x_translation/doe"):
        os.makedirs("ecta2024_data/x_translation/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: x translation.")
    for d_x in range(1, 101):
        tvec = np.random.uniform(-1, 1, 10) * d_x
        input_x = x.T.copy()
        for j in range(input_x.shape[1]):
            input_x[:, j] += tvec
        problem.values(input_x)
        results = problem.ObjFunc
        file_name = f"ecta2024_data/x_translation/doe/{pid}_{d_x:.6f}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, results)

def y_scaling(problem):
    if not os.path.exists("ecta2024_data/y_scaling/doe"):
        os.makedirs("ecta2024_data/y_scaling/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: y scaling.")
    y = np.loadtxt(f"ecta2024_data/origin/doe/{pid}.txt")
    for log_k in range(-30, 31, 1):
        if log_k == 0:
            continue
        k = 2**(log_k/10.0)
        Y = y.copy() * k
        file_name = f"ecta2024_data/y_scaling/doe/{pid}_{log_k/10:.6f}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, Y)


def y_translation(problem):
    if not os.path.exists("ecta2024_data/y_translation/doe"):
        os.makedirs("ecta2024_data/y_translation/doe")
    pid = problem.func
    print(f"Processing: problem id: {pid}, transformation: y translation.")
    y = np.loadtxt(f"ecta2024_data/origin/doe/{pid}.txt")
    for d_y in range(50, 1001, 50):
        Y = y.copy() + d_y
        file_name = f"ecta2024_data/y_translation/doe/{pid}_{d_y}.txt"
        print(f"Saving to {file_name}")
        np.savetxt(file_name, Y)


def transformations(problem_id, x):
    rvec_file_path = "config/random_look_10d_rotation_matrices.txt"
    array = read_matrices_to_array(rvec_file_path)
    problem = CEC2022.cec2022_func(problem_id)
    save_origin(problem, x)
    x_rotation(problem, array, x)
    x_scaling(problem, x)
    x_translation(problem, x)
    y_scaling(problem)
    y_translation(problem)


if __name__ == "__main__":
    if not os.path.exists("config/samplingDOE.txt"):
        obj = doe_model(dim=10, m=8, latent_dim=32, kl_weight=0.001,
                        use_mlflow=False, model_type="VAE")
        obj.load_from_huggingface()
        sample = obj.sample * 200 - 100
        np.savetxt("config/samplingDOE.txt", sample)
    x = np.loadtxt("config/samplingDOE.txt")
    for problem_id in range(1, 13):
        transformations(problem_id, x)