import re
import numpy as np
from doe2vec import doe_model


def encode_origin(problem_id, obj):
    file_path = f"ecta2024_data/origin/doe/{problem_id}.txt"
    cec_y = np.loadtxt(file_path)
    # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
    y = cec_y.flatten()
    encoded = obj.encode([y])
    return encoded[0]


def encode_x_rotation(problem_id, obj):
    vecs = []
    for matrix_id in range(100):
        file_path = f"ecta2024_data/x_rotation/doe/{problem_id}_{matrix_id}.txt"
        cec_y = np.loadtxt(file_path)
        # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
        y = cec_y.flatten()
        encoded = obj.encode([y])
        vecs += [encoded[0].tolist()]
    return vecs


def encode_x_scaling(problem_id, obj):
    vecs = []
    for log_k in range(-30, 31, 1):
        if log_k == 0:
            continue
        file_path = f"ecta2024_data/x_scaling/doe/{problem_id}_{log_k/10:.6f}.txt"
        cec_y = np.loadtxt(file_path)
        # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
        y = cec_y.flatten()
        encoded = obj.encode([y])
        vecs += [encoded[0].tolist()]
    return vecs


def encode_x_translation(problem_id, obj):
    vecs = []
    for d_x in range(1, 101):
        file_path = f"ecta2024_data/x_translation/doe/{problem_id}_{d_x:.6f}.txt"
        cec_y = np.loadtxt(file_path)
        # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
        y = cec_y.flatten()
        encoded = obj.encode([y])
        vecs += [encoded[0].tolist()]
    return vecs


def encode_y_scaling(problem_id, obj):
    vecs = []
    for log_k in range(-30, 31, 1):
        if log_k == 0:
            continue
        file_path = f"ecta2024_data/y_scaling/doe/{problem_id}_{log_k/10:.6f}.txt"
        cec_y = np.loadtxt(file_path)
        # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
        y = cec_y.flatten()
        encoded = obj.encode([y])
        vecs += [encoded[0].tolist()]
    return vecs


def encode_y_translation(problem_id, obj):
    vecs = []
    for d_y in range(50, 1001, 50):
        file_path = f"ecta2024_data/y_translation/doe/{problem_id}_{d_y}.txt"
        cec_y = np.loadtxt(file_path)
        # y = (cec_y.flatten() - np.min(cec_y)) / (np.max(cec_y) - np.min(cec_y))
        y = cec_y.flatten()
        encoded = obj.encode([y])
        vecs += [encoded[0].tolist()]
    return vecs


if __name__ == "__main__":
    obj = doe_model(dim=10, m=8, latent_dim=32, kl_weight=0.001,
                    use_mlflow=False, model_type="VAE")
    obj.load_from_huggingface()
    vecs = [[] for _ in range(6)]
    for problem_id in range(1, 13):
        vecs[0] += [encode_origin(problem_id, obj).tolist()]
        vecs[1] += encode_x_rotation(problem_id, obj)
        vecs[2] += encode_x_scaling(problem_id, obj)
        vecs[3] += encode_x_translation(problem_id, obj)
        vecs[4] += encode_y_scaling(problem_id, obj)
        vecs[5] += encode_y_translation(problem_id, obj)
    for i in range(6):
        print(np.array(vecs[i]).shape)
    np.savetxt("ecta2024_data/origin/doe/vecs.txt", np.array(vecs[0]))
    np.savetxt("ecta2024_data/x_rotation/doe/vecs.txt", np.array(vecs[1]))
    np.savetxt("ecta2024_data/x_scaling/doe/vecs.txt", np.array(vecs[2]))
    np.savetxt("ecta2024_data/x_translation/doe/vecs.txt", np.array(vecs[3]))
    np.savetxt("ecta2024_data/y_scaling/doe/vecs.txt", np.array(vecs[4]))
    np.savetxt("ecta2024_data/y_translation/doe/vecs.txt", np.array(vecs[5]))
