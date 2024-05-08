import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def rotation_avg(x, y):
    bins = np.linspace(-2, 2, 21)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    y_means = []
    for i in range(len(bins)-1):
        bin_mask = (x >= bins[i]) & (x < bins[i+1])
        bin_y_values = y[bin_mask]
        y_means.append(bin_y_values.mean())
    y_means = np.array(y_means)
    return bin_centers, y_means


def lineplot(transformation, indicator, ax1, conn):
    print(f"Plotting {transformation}.")
    sql_query = f"SELECT * FROM {transformation}_ks_pvalue"
    df_ks_pvalue = pd.read_sql_query(sql_query, conn)
    sql_query = f"SELECT * FROM {transformation}_emd"
    df_emd = pd.read_sql_query(sql_query, conn)
    ax2 = ax1.twinx()
    for problem_id in range(1, 13):
        if problem_id > 5 and transformation not in ["y_translation", "y_scaling",]:
            continue
        selected_pvalue = df_ks_pvalue[df_ks_pvalue["problem_id"]
                                       == problem_id].values
        columns_to_check = selected_pvalue[:, 2:]
        counts = np.sum(columns_to_check < 0.05, axis=1)
        number_of_columns = columns_to_check.shape[1]
        ratios = counts / number_of_columns
        selected_pvalue[:, 2] = ratios
        if transformation == "x_rotation":
            x, y = rotation_avg(selected_pvalue[:, 1], selected_pvalue[:, 2])
        else:
            first_positive_index = np.where(selected_pvalue[:, 1] > 0)[0][0]
            x = np.insert(selected_pvalue[:, 1], first_positive_index, 0.)
            y = np.insert(selected_pvalue[:, 2], first_positive_index, 0.)
        ax1.plot(x, y, label=f"problem {problem_id}")
        selected_emd = df_emd[df_emd["problem_id"] == problem_id].values
        columns_to_check = selected_emd[:, 2:]
        counts = np.sum(columns_to_check, axis=1)
        selected_emd[:, 2] = counts
        if transformation == "x_rotation":
            x, y = rotation_avg(selected_emd[:, 1], selected_emd[:, 2])
        else:
            x = np.insert(selected_emd[:, 1], first_positive_index, 0.)
            y = np.insert(selected_emd[:, 2], first_positive_index, 0.)
        ax2.plot(x, y, linestyle="dotted", label=f"problem {problem_id} (EMD)")
    ax1.set_xlabel(f"${indicator}$")
    ax1.set_ylabel('Percentage of changed ELA features', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_ylabel("EMD", color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    ax1.set_title(f"{transformation}")
    ax1.legend()


if __name__ == "__main__":
    if not os.path.exists("results/aggregation/"):
        os.mkdir("results/aggregation/")
    transformations = ["x_translation",
                       "y_translation",
                       "x_scaling",
                       "y_scaling",
                       "x_rotation",]
    indicator = ["d_x",
                 "d_y",
                 "log_2^k",
                 "log_2^k",
                 "trace",]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axs = plt.subplots(3, 2, figsize=(15, 13))
    axs = axs.ravel()
    axs[5].axis('off')
    for i in range(len(transformations)):
        lineplot(transformations[i], indicator[i], axs[i], conn)
    # plt.subplots_adjust(left=0.1, right=0.8, top=0.95,
    #                     bottom=0.05, hspace=0.4, wspace=0.35)
    plt.tight_layout()
    plt.savefig(f"results/aggregation/results.png")
    plt.cla()
    print("Done!")
