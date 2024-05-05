import numpy as np


def generate_tvec(low, high):
    arr = np.zeros(10)
    special_index = np.random.randint(0, 10)
    arr[special_index] = np.random.uniform(
        low, high) * np.random.choice([-1, 1])
    for i in range(10):
        if i != special_index:
            arr[i] = np.random.uniform(-high, high)
    return arr


tvecs = []
for i in range(50):
    for j in range(20):
        low = j * 5
        high = low + 5
        tvec = generate_tvec(low, high)
        tvecs += [tvec.tolist()]
np.savetxt("config/tvec.txt", np.array(tvecs))

tvecs = np.loadtxt("config/tvec.txt")
tvec_l1 = np.max(np.abs(tvecs), axis=1)
