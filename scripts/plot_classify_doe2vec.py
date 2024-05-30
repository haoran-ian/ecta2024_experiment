import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def diff(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cos_theta = dot_product / (norm_a * norm_b)
    cos_theta = np.clip(cos_theta, -1, 1)
    theta_radians = np.arccos(cos_theta)
    theta_degrees = np.degrees(theta_radians)
    return theta_degrees


def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euc_dis(a, b):
    return np.linalg.norm(a - b)

def load_vecs():
    vecs = np.loadtxt("ecta2024_data/origin/doe/vecs.txt")
    normalized_vecs = vecs.copy()
    # for i in range(vecs.shape[1]):
    #     min_val = vecs[:, i].min()
    #     max_val = vecs[:, i].max()
    #     if max_val != min_val:
    #         normalized_vecs[:, i] = (vecs[:, i] - min_val) / (max_val - min_val)
    #     else:
    #         normalized_vecs[:, i] = 0
    return normalized_vecs


def load_elas():
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    query = "SELECT * FROM origin"
    df = pd.read_sql_query(query, conn)
    for column in df.columns[1:]:
        min_val = df[column].min()
        max_val = df[column].max()
        if max_val != min_val:
            df[column] = (df[column] - min_val) / (max_val - min_val) * 2 - 1
        else:
            df[column] = 0
    elas = df.groupby(["problem_id"]).mean().values
    return elas


if __name__ == "__main__":
    matrix = [[None for _ in range(12)] for _ in range(12)]
    vecs = load_vecs()
    elas = load_elas()
    print(vecs)
    for i in range(12):
        for j in range(12):
            if i >= j:
                matrix[i][j] = cos_sim(vecs[i], vecs[j])
            else:
                matrix[i][j] = cos_sim(elas[i], elas[j])
    df = pd.DataFrame(matrix, columns=[str(i+1) for i in range(12)],
                      index=[str(i+1) for i in range(12)])
    plt.style.use("seaborn-v0_8-darkgrid")
    ax = sns.heatmap(df, cmap="viridis", square=True, annot=True,
                     fmt=".2f", cbar_kws={"label": "cosine similarity"}) 
    ax.set(xlabel="problem id", ylabel="problem id")
    plt.tight_layout()
    plt.savefig("results/classify.png")
