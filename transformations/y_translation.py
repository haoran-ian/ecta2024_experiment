import os
import numpy as np

if not os.path.exists("ecta2024_data/y_translation/"):
    os.makedirs("ecta2024_data/y_translation/")

for problem_id in range(1, 13):
    file_path = f"ecta2024_data/origin/{problem_id}_0.000000.txt"
    array = np.loadtxt(file_path)
    for dy in range(50, 1001, 50):
        new_array = array + dy
        np.savetxt(
            f"ecta2024_data/y_translation/{problem_id}_{dy}.txt", new_array)
