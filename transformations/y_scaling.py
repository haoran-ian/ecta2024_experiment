import os
import numpy as np

if not os.path.exists("ecta2024_data/y_scaling/"):
    os.makedirs("ecta2024_data/y_scaling/")

for problem_id in range(1, 13):
    file_path = f"ecta2024_data/origin/{problem_id}_0.000000.txt"
    array = np.loadtxt(file_path)
    for log_k in range(-30, 31, 1):
        if log_k == 0:
            continue
        new_array = array * 2**(log_k/10)
        np.savetxt(
            f"ecta2024_data/y_scaling/{problem_id}_{log_k/10:.6f}.txt",
            new_array)
