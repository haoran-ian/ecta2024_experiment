import os
import numpy as np

folder = "ecta2024_data/x_rotation/"
file_paths = os.listdir(folder)

for file_path in file_paths:
    array = np.loadtxt(f"{folder}{file_path}")
    print(np.min(array))