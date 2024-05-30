import copy
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from umap import UMAP


def format_labels(header):
    """Format header to string by problem_id, is_subtract, is_rotate, is_scale.

    Args:
        header (numpy array): labels

    Returns:
        list: formatted labels
        list: colors
    """
    marker_size = 20
    # set 5 colors for 5 problems, consider color blindness
    base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                   '#aec7e8', '#ffbb78']
    # Adjust transparency of base_colors according to subtract_lim or
    # scale_factor
    label = "problem {}".format(int(header[0]))
    if int(header[5]) == 1:
        label += ", random translation limit: {}".format(header[2])
        # # map subtract_lim (90, 60, 30) to alpha (0.2, 0.5, 0.8)
        # if float(header[2]) == 90. or float(header[2]) == 900.:
        #     alpha = 0.2
        # elif float(header[2]) == 60. or float(header[2]) == 600.:
        #     alpha = 0.5
        # else:
        #     alpha = 0.8
        alpha = 1
        marker = "v"
        s = marker_size * alpha
    elif int(header[6]) == 1:
        label += ", random rotation."
        alpha = 1
        marker = "D"
        s = marker_size * alpha
    elif int(header[7]) == 1:
        label += ", scale factor: {}".format(header[4])
        # top = np.abs(np.log2(float(header[4])))
        # if top == 3.:
        #     alpha = 0.2
        # elif top == 2.:
        #     alpha = 0.5
        # else:
        #     alpha = 0.8
        alpha = 1
        marker = "<" if float(header[4]) < 1 else ">"
        s = marker_size * alpha
    else:
        alpha = 1
        marker = "o"
        s = 20
    color = base_colors[int(header[0]) - 1] + "{:02x}".format(int(255 * alpha))
    # color = base_colors[int(header[0]) - 1]
    return label, color, marker, s


def legend_elements(type):
    """Get legend elements.

    Args:
        type (str): "raw", "subtract", "rotate", "scale"

    Returns:
        list: legend elements
    """
    marker_size = 200
    # set 5 colors for 5 problems, consider color blindness
    base_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                   '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                   '#aec7e8', '#ffbb78']
    # define legend
    legend_elements = []
    for i in range(12):
        line = plt.Line2D([0], [0], marker='o', color='w',
                          label='problem {}'.format(i + 1),
                          markerfacecolor=base_colors[i],
                          markersize=50**0.5)
        # set marker edge color to black
        line.set_markeredgecolor('black')
        legend_elements.append(line)
    if type == "subtract":
        alphas = [0.8, 0.5, 0.2]
        for i in range(3):
            # map subtract_lim (90, 60, 30) to alpha (0.2, 0.5, 0.8)
            alpha = alphas[i]
            color = "#000000{:02x}".format(int(255 * alpha))
            s = marker_size * alpha
            line = plt.Line2D([0], [0], marker='v', color='w',
                              label='translation limit: {}'.format(30.*(i+1)),
                              markerfacecolor=color, markersize=s**0.5)
            # set marker edge color to black
            line.set_markeredgecolor('black')
            legend_elements.append(line)
    if type == "rotate":
        line = plt.Line2D([0], [0], marker='x', color='w',
                          label='random rotation',
                          markersize=20**0.5)
        # set marker edge color to black
        line.set_markeredgecolor('black')
        legend_elements.append(line)
    if type == "scale":
        alphas = [0.8, 0.5, 0.2]
        for i in range(3):
            alpha = alphas[i]
            color = "#000000{:02x}".format(int(255 * alpha))
            s = marker_size * alpha
            line = plt.Line2D([0], [0], marker='>', color='w',
                              label='scale factor: {}'.format(2**(i+1)),
                              markerfacecolor=color, markersize=s**0.5)
            # set marker edge color to black
            line.set_markeredgecolor('black')
            legend_elements.append(line)
        for i in range(3):
            alpha = alphas[i]
            color = "#000000{:02x}".format(int(255 * alpha))
            s = marker_size * alpha
            line = plt.Line2D([0], [0], marker='<', color='w',
                              label='scale factor: {}'.format(0.5**(i+1)),
                              markerfacecolor=color, markersize=s**0.5)
            # set marker edge color to black
            line.set_markeredgecolor('black')
            legend_elements.append(line)
    return legend_elements


def fit_reducer(samples):
    """Fit umap to samples.

    Args:
        samples (numpy array): samples

    Returns:
        umap object: umap object
    """
    # fit umap
    reducer = UMAP(n_components=2, n_neighbors=20, min_dist=0.9,
                   metric='euclidean', random_state=42)
    reducer.fit(samples)
    return reducer


def plot_reducer(ax, reducer, samples, labels, title, origin=False):
    """Plot LDA.

    Args:
        lda (sklearn.discriminant_analysis.LinearDiscriminantAnalysis): LDA
        samples (numpy array): samples
        y (numpy array): labels
    """
    plot_rate = 0.1
    # plot LDA
    X = reducer.transform(samples)
    is_subtract = False
    is_rotate = False
    is_scale = False
    for i in range(len(labels)):
        is_subtract = True if labels[i][5] == 1 else is_subtract
        is_rotate = True if labels[i][6] == 1 else is_rotate
        is_scale = True if labels[i][7] == 1 else is_scale
        is_trans = labels[i][5] == 1 or labels[i][6] == 1 or labels[i][7] == 1
        if is_trans and np.random.rand() > plot_rate:
            continue
        _, color, marker, s = format_labels(labels[i])
        if not origin and not is_trans:
            ax.scatter(-X[i, 0], X[i, 1], facecolors=color, marker=marker,
                       s=s, edgecolors='black', linewidths=0.2, alpha=0.2)
        else:
            ax.scatter(-X[i, 0], X[i, 1], facecolors=color, marker=marker,
                       s=s, edgecolors='black', linewidths=0.2)
    ax.set_title(title)
    # set legend
    legend_type = "subtract" if is_subtract else "rotate" if is_rotate else \
        "scale" if is_scale else "raw"
    # ax.set_xlabel("Component 1")
    # ax.set_ylabel("Component 2")
    # ax.set_aspect('equal', adjustable='box')
    # locate at bottom left, size is slightly smaller than default, 2 columns
    # ax.legend(handles=legend_elements(legend_type),
    #           loc='lower left', ncol=2, fontsize=9)
    plt.savefig(f"results/{title}.png")


def convert_labels(labels, case="origin"):
    results = []
    for l in labels:
        if case == "origin":
            results += [[l, 0, 0, 0, 0, 0, 0, 0]]
        elif case == "x_translation":
            results += [[l[0], 0, l[1], 0, 0, 1, 0, 0]]
        elif case == "y_translation":
            results += [[l[0], 0, l[1], 0, 0, 1, 0, 0]]
        elif case == "x_scaling":
            results += [[l[0], 0, 0, 0, l[1], 0, 0, 1]]
        elif case == "y_scaling":
            results += [[l[0], 0, 0, 0, l[1], 0, 0, 1]]
        elif case == "x_rotation":
            results += [[l[0], 0, 0, l[1], 0, 0, 1, 0]]
    return results


if __name__ == "__main__":
    transformations = ["x_translation",
                       "y_translation",
                       "x_scaling",
                       "y_scaling",
                       "x_rotation",]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axs = plt.subplots(3, 2, figsize=(8, 8))
    axs = axs.ravel()

    sql_query = f"SELECT * FROM origin"
    df = pd.read_sql_query(sql_query, conn)
    origin_samples = df.values[:, 1:]
    origin_labels = df.values[:, 0]
    origin_labels = convert_labels(origin_labels)
    reducer = fit_reducer(origin_samples)
    plot_reducer(axs[0], reducer, origin_samples,
                 origin_labels, title="origin", origin=True)

    for i in range(len(transformations)):
        transformation = transformations[i]
        sql_query = f"SELECT * FROM {transformation}"
        df = pd.read_sql_query(sql_query, conn)
        samples = df.values[:, 2:]
        labels = df.values[:, :2]
        labels = convert_labels(labels, transformation)
        samples = np.concatenate((origin_samples, samples))
        labels = np.concatenate((origin_labels, labels))
        plot_reducer(axs[i+1], reducer, samples, labels, title=transformation)

    plt.tight_layout()
    plt.legend()
    plt.savefig("results/umap.png")
    plt.savefig("results/umap.eps")
