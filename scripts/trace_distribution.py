import numpy as np
import matplotlib.pyplot as plt


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


if __name__ == "__main__":
    array = np.loadtxt("config/100_10d_rotation_matrices.txt").tolist()
    rotation_matrices = [np.array(array[10*i:10*(i+1)]) for i in range(100)]
    # Calculate the trace for each rotation matrix
    traces = [np.trace(matrix) for matrix in rotation_matrices]
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(6, 3.5))
    plt.hist(traces, bins=20, range=(-3.0, 2.0), alpha=0.7)
    plt.title('Random Sampling $R \in \mathbb{R}^{10} \\times \mathbb{R}^{10}$')
    plt.xlabel('Trace')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/trace_distribution.png")
    plt.cla()

    filename = "config/random_look_10d_rotation_matrices.txt"
    rotation_matrices = read_matrices_to_array(filename)
    # traces = [np.trace(matrix) for matrix in rotation_matrices]
    traces = [np.trace(matrix) for matrix in rotation_matrices]
    plt.style.use("seaborn-v0_8-darkgrid")
    plt.figure(figsize=(6, 3.5))
    plt.hist(traces, bins=20, range=(-2.0, 2.0), alpha=0.7)
    plt.title('Rejection Sampling $R \in \mathbb{R}^{10} \\times \mathbb{R}^{10}$')
    plt.xlabel('Trace')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("results/controlled_trace_distribution.png")
    plt.cla()
