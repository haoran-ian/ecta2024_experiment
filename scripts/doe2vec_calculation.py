import re
import numpy as np
from doe2vec import doe_model


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

x = read_x(100, 1000)
x = x[0][:100, :]
print(x.shape)
obj = doe_model(10, 1, n=1000000, latent_dim=32, custom_sample=x,
                model_type="VAE", kl_weight=0.001, use_mlflow=False)
if not obj.loadModel("../models"):
    obj.generateData()
    obj.compile()
    obj.fit(100)
    obj.save()
