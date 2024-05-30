import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


if __name__ == "__main__":
    transformations = ["x_translation", "y_translation", "x_scaling",
                       "y_scaling", "x_rotation",]
    titles = ["translation on $\\boldsymbol{x}$", "translation on $y$",
              "scaling on $\\boldsymbol{x}$", "scaling on $y$",
              "rotation on $\\boldsymbol{x}$"]
    values = np.zeros((len(transformations), 55, 12))
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    fig, axs = plt.subplots(1, 5, figsize=(18, 12))
    axs = axs.flatten()
    plt.rcParams['font.family'] = 'Times New Roman'
    plt.style.use("seaborn-v0_8-darkgrid")
    for i in range(len(transformations)):
        df = pd.read_sql_query(
            f"SELECT * FROM {transformations[i]}_ks_pvalue", conn)
        for problem_id in range(1, 13):
            df_pid = df[(df["problem_id"] == problem_id)]
            array = df_pid.values[:, 2:]
            keys = df_pid.columns[2:]
            for j in range(55):
                values[i, j, problem_id -
                       1] = np.sum(array[:, j] < 0.05) / array.shape[0]
        df_heatmap = pd.DataFrame(values[i], index=keys,
                                  columns=[str(i+1) for i in range(12)])
        if i == 0:
            sns.heatmap(df_heatmap, cmap="viridis", square=True, cbar=False,
                        ax=axs[i])
        elif i == 4:
            sns.heatmap(df_heatmap, cmap="viridis", square=True, cbar=True,
                        yticklabels=False, ax=axs[i],
                        cbar_kws={"label": "sensitivity"})
        else:
            sns.heatmap(df_heatmap, cmap="viridis", square=True, cbar=False,
                        yticklabels=False, ax=axs[i])
        axs[i].set_title(titles[i])
    fig.supxlabel("problem id")
    plt.tight_layout()
    plt.savefig(f"results/sensitivity/heatmap.png")
    plt.close()
