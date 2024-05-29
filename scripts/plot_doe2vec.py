import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.colors as mcolors
import pandas as pd


def diff(a, b):
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cos_theta = dot_product / (norm_a * norm_b)
    return cos_theta


def aggregate_diff(a, list_b):
    return [diff(a, b) for b in list_b]


def lineplot(transformation, indicator, ax1):
    print(f"Plotting {transformation}.")
    origin = np.loadtxt("ecta2024_data/origin/doe/vecs.txt")
    if transformation == "x_rotation":
        x = np.array([-1.9 + i * 0.2 for i in range(20)])
        vecs = np.loadtxt("ecta2024_data/x_rotation/doe/vecs.txt")
        diffs = np.array([aggregate_diff(origin[i], vecs[100*i:100*(i+1)])
                          for i in range(12)])
        values = []
        for i in range(12):
            for j in range(100):
                values += [[i+1, x[int(j/5)], diffs[i, j]]]
        df = pd.DataFrame(values, columns=["problem_id", "x", "diff"])
    elif transformation == "x_translation":
        x = [1.0 + i for i in range(100)]
        vecs = np.loadtxt("ecta2024_data/x_translation/doe/vecs.txt")
        diffs = np.array([aggregate_diff(origin[i], vecs[100*i:100*(i+1)])
                          for i in range(12)])
        values = []
        for i in range(12):
            for j in range(100):
                values += [[i+1, x[j], diffs[i, j]]]
        df = pd.DataFrame(values, columns=["problem_id", "x", "diff"])
        for problem_id in range(1, 13):
            df.loc[len(df)] = [problem_id, 0, 1]
        sorted_df = df.sort_values(by="x")
        sorted_df["Moving_Avg"] = sorted_df["diff"].rolling(window=5).mean()
        result_df = df.copy()
        result_df["diff"] = sorted_df['Moving_Avg'].values
        df = result_df
    elif transformation == "y_translation":
        x = [5.0 + i * 5 for i in range(20)]
        vecs = np.loadtxt("ecta2024_data/y_translation/doe/vecs.txt")
        diffs = np.array([aggregate_diff(origin[i], vecs[20*i:20*(i+1)])
                          for i in range(12)])
        values = []
        for i in range(12):
            for j in range(20):
                values += [[i+1, x[j], diffs[i, j]]]
        df = pd.DataFrame(values, columns=["problem_id", "x", "diff"])
        for problem_id in range(1, 13):
            df.loc[len(df)] = [problem_id, 0, 1]
    else:
        x = [(i-30)/10 for i in range(30)] + [(i+1)/10 for i in range(30)]
        vecs = np.loadtxt(f"ecta2024_data/{transformation}/doe/vecs.txt")
        diffs = np.array([aggregate_diff(origin[i], vecs[60*i:60*(i+1)])
                          for i in range(12)])
        values = []
        for i in range(12):
            for j in range(60):
                values += [[i+1, x[j], diffs[i, j]]]
        df = pd.DataFrame(values, columns=["problem_id", "x", "diff"])
        for problem_id in range(1, 13):
            df.loc[len(df)] = [problem_id, 0, 1]
    # print(diffs.shape, x.shape)
    # print(x)
    for problem_id in range(1, 13):
        sns.lineplot(x="x", y="diff", data=df[df["problem_id"] == problem_id],
                     color=colors[problem_id-1], marker=markers[problem_id-1],
                     markersize=4, markerfacecolor=marker_colors[problem_id-1],
                     markeredgecolor=colors[problem_id-1],
                     ax=ax1)
        # selected_y = df[df["problem_id"] == problem_id].values
        # if transformation == "x_rotation":
        #     x, y = rotation_avg(selected_pvalue[:, 1], selected_pvalue[:, 2])
        # else:
        #     first_positive_index = np.where(selected_pvalue[:, 1] > 0)[0][0]
        #     x = np.insert(selected_pvalue[:, 1], first_positive_index, 0.)
        #     y = np.insert(selected_pvalue[:, 2], first_positive_index, 0.)
        # ax1.plot(x, y, color=colors[problem_id-1], marker=markers[problem_id-1],
        #          markersize=4, markerfacecolor=marker_colors[problem_id-1],)
    if indicator == "trace":
        indicator = "\\text{Tr}(R)"
    ax1.set_xlabel(f"${indicator}$")
    ax1.set_ylabel('Cosine Similarity of Changed DoE2Vec results', color='g')
    # ax1.tick_params(axis='y', labelcolor='g')
    # ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    # ax2.set_ylabel("EMD", color='b')
    # ax2.tick_params(axis='y', labelcolor='b')
    # ax1.set_title(f"{transformation}")


if __name__ == "__main__":
    if not os.path.exists("results/doe2vec/"):
        os.mkdir("results/doe2vec/")
    problem_type = ["Unimodal", "Basic", "Basic", "Basic", "Basic", "Hybrid",
                    "Hybrid", "Hybrid", "Composition", "Composition",
                    "Composition", "Composition"]
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
    plt.style.use("seaborn-v0_8-darkgrid")

    for i in range(len(transformations)):
        fig, ax = plt.subplots(figsize=(8, 4))
        lineplot(transformations[i], indicator[i], ax)
        plt.tight_layout()
        plt.savefig(f"results/doe2vec/{transformations[i]}.png", dpi=400)
        plt.cla()
    fig, ax = plt.subplots(figsize=(8, 4))
    for problem_id in range(1, 13):
        ax.plot([], [], color=colors[problem_id-1],
                marker=markers[problem_id-1],
                markersize=4, label=f"No. {problem_id}, {problem_type[problem_id-1]} (DOE2Vec)",
                markerfacecolor=marker_colors[problem_id-1])
        # axs[0].plot([], [], color=colors[problem_id-1], linestyle="dashed",
        #             label=build_label(problem_id, "doe2vec"))
    ax.legend(loc='center', ncol=2)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(f"results/doe2vec/legend.png", dpi=400)
    plt.cla()
