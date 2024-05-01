import numpy as np

np.random.seed(42)

tvec = np.random.uniform(-100.0, 100.0, size=(1000, 10))
np.savetxt("config/tvec.txt", tvec)