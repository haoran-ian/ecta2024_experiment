import os
import sqlite3
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.colors as mcolors


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


def build_label(problem_id, measurement):
    problem_type = ["Unimodal", "Basic", "Basic", "Basic", "Basic", "Hybrid",
                    "Hybrid", "Hybrid", "Composition", "Composition",
                    "Composition", "Composition"]
    if measurement == "kstest":
        return f"No. {problem_id}, {problem_type[problem_id-1]}\n(Percentage of changed ELA features)"
    elif measurement == "emd":
        return f"No. {problem_id}, {problem_type[problem_id-1]} (EMD)"
    elif measurement == "doe2vec":
        return f"No. {problem_id}, {problem_type[problem_id-1]} (DOE2Vec)"


def lineplot(transformation, indicator, ax1, conn):
    print(f"Plotting {transformation}.")
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']
    markers = ['o', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '^', '<']
    marker_colors = [mcolors.to_rgba(color, alpha=0.5) for color in colors]
    sql_query = f"SELECT * FROM {transformation}_ks_pvalue"
    df_ks_pvalue = pd.read_sql_query(sql_query, conn)
    sql_query = f"SELECT * FROM {transformation}_emd"
    df_emd = pd.read_sql_query(sql_query, conn)
    ax2 = ax1.twinx()
    for problem_id in range(1, 13):
        selected_pvalue = df_ks_pvalue[df_ks_pvalue["problem_id"]
                                       == problem_id].values
        columns_to_check = selected_pvalue[:, 2:]
        counts = np.sum(columns_to_check < 0.05, axis=1)
        number_of_columns = columns_to_check.shape[1]
        ratios = counts / number_of_columns
        selected_pvalue[:, 2] = ratios
        if transformation == "x_rotation":
            # x, y = rotation_avg(selected_pvalue[:, 1], selected_pvalue[:, 2])
            x = np.array([-1.9 + i * 0.2 for i in range(20) for _ in range(5)])
            y = selected_pvalue[:, 2]
        else:
            first_positive_index = np.where(selected_pvalue[:, 1] > 0)[0][0]
            x = np.insert(selected_pvalue[:, 1], first_positive_index, 0.)
            y = np.insert(selected_pvalue[:, 2], first_positive_index, 0.)
            if transformation == "x_translation":
                df = pd.DataFrame(y, columns=["y"])
                df["avg_y"] = df["y"].rolling(window=5).mean()
                y = df["avg_y"].values
        df = pd.DataFrame(np.vstack([x, y]).T, columns=["x", "y"])
        sns.lineplot(x="x", y="y", data=df, color=colors[problem_id-1],
                     marker=markers[problem_id-1], markersize=4,
                     markerfacecolor=marker_colors[problem_id-1],
                     markeredgecolor=colors[problem_id-1], ax=ax1)
        # ax1.plot(x, y, color=colors[problem_id-1], marker=markers[problem_id-1],
        #          markersize=4, markerfacecolor=marker_colors[problem_id-1],)
        # plot EMD
        selected_emd = df_emd[df_emd["problem_id"] == problem_id].values
        columns_to_check = selected_emd[:, 2:]
        counts = np.sum(columns_to_check, axis=1)
        selected_emd[:, 2] = counts
        if transformation == "x_rotation":
            x, y = rotation_avg(selected_emd[:, 1], selected_emd[:, 2])
        else:
            x = np.insert(selected_emd[:, 1], first_positive_index, 0.)
            y = np.insert(selected_emd[:, 2], first_positive_index, 0.)
            if transformation == "x_translation":
                df = pd.DataFrame(y, columns=["y"])
                df["avg_y"] = df["y"].rolling(window=5).mean()
                y = df["avg_y"].values
        ax2.plot(x, y, linestyle="dotted")
    if indicator == "trace":
        indicator = "\\text{Tr}(R)"
    ax1.set_xlabel(f"${indicator}$")
    ax1.set_ylabel('Percentage of changed ELA features', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_ylabel("EMD", color='b')
    ax2.tick_params(axis='y', labelcolor='b')


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
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
              '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8', '#ffbb78']
    markers = ['o', 's', 'p', '*', 'h', 'H', '+', 'x', 'D', 'd', '^', '<']
    marker_colors = [mcolors.to_rgba(color, alpha=0.5) for color in colors]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    plt.style.use("seaborn-v0_8-darkgrid")
    for i in range(len(transformations)):
        fig, ax = plt.subplots(figsize=(8, 4))
        lineplot(transformations[i], indicator[i], ax, conn)
        plt.tight_layout()
        plt.savefig(f"results/aggregation/{transformations[i]}.png", dpi=400)
        plt.cla()
    fig, ax = plt.subplots(figsize=(8, 4))
    for problem_id in range(1, 13):
        ax.plot([], [], color=colors[problem_id-1],
                marker=markers[problem_id-1],
                markersize=4, label=build_label(problem_id, "kstest"),
                markerfacecolor=marker_colors[problem_id-1])
        ax.plot([], [], color=colors[problem_id-1], linestyle="dotted",
                label=build_label(problem_id, "emd"))
    ax.legend(loc='lower center', ncol=2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"results/aggregation/legend.png", dpi=400)
    plt.cla()
