import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


def string_to_list(string):
    string = string[1:-1]
    content = string.split(", ")
    return [float(c) for c in content]


def lineplot(transformation, indicator, ax1, conn):
    print(f"Plotting {transformation}.")
    plt.style.use("seaborn-v0_8-darkgrid")
    sql_query = f"SELECT * FROM {transformation}_ks_statistic"
    df_ks_statistic = pd.read_sql_query(sql_query, conn)
    sql_query = f"SELECT * FROM {transformation}_ks_pvalue"
    df_ks_pvalue = pd.read_sql_query(sql_query, conn)
    sql_query = f"SELECT * FROM {transformation}_emd"
    df_emd = pd.read_sql_query(sql_query, conn)
    # fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    for problem_id in range(1, 6):
        selected_pvalue = df_ks_pvalue[df_ks_pvalue["problem_id"]
                                       == problem_id].values
        columns_to_check = selected_pvalue[:, 2:]
        counts = np.sum(columns_to_check < 0.05, axis=1)
        number_of_columns = columns_to_check.shape[1]
        ratios = counts / number_of_columns
        selected_pvalue[:, 2] = ratios
        first_positive_index = np.where(selected_pvalue[:, 1] > 0)[0][0]
        x = np.insert(selected_pvalue[:, 1], first_positive_index, 0.)
        y = np.insert(selected_pvalue[:, 2], first_positive_index, 0.)
        ax1.plot(x, y, label=f"problem {problem_id}")
        selected_emd = df_emd[df_emd["problem_id"] == problem_id].values
        columns_to_check = selected_emd[:, 2:]
        counts = np.sum(columns_to_check, axis=1)
        selected_emd[:, 2] = counts
        x = np.insert(selected_emd[:, 1], first_positive_index, 0.)
        y = np.insert(selected_emd[:, 2], first_positive_index, 0.)
        # ax2 = ax1.twinx()
        ax2.plot(x, y, linestyle="dotted", label=f"problem {problem_id} (EMD)")
    ax1.set_xlabel(f"${indicator}$")
    ax1.set_ylabel('Percentage of changed ELA features', color='g')
    ax1.tick_params(axis='y', labelcolor='g')
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1))
    ax2.set_ylabel("EMD", color='b')
    ax2.tick_params(axis='y', labelcolor='b')
    ax1.legend()
    # plt.tight_layout()
    # plt.savefig(f"results/aggregation/{transformation}.png")
    # plt.cla()


if __name__ == "__main__":
    if not os.path.exists("results/aggregation/"):
        os.mkdir("results/aggregation/")
    transformations = ["y_translation", "x_scaling", "y_scaling",]
    indicator = ["log_2^k", "log_2^k", "d_y"]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    plt.style.use("seaborn-v0_8-darkgrid")
    fig, axs = plt.subplots(3, 2, figsize=(20, 18))
    axs = axs.ravel()
    axs[5].axis('off')
    for i in range(len(transformations)):
        lineplot(transformations[i], indicator[i], axs[i], conn)
    # plt.subplots_adjust(left=0.1, right=0.8, top=0.95,
    #                     bottom=0.05, hspace=0.4, wspace=0.35)
    plt.tight_layout()
    plt.savefig(f"results/aggregation/results.png")
    plt.cla()

# factors = [0.015625, 0.03125, 0.0625, 0.125, 0.25, 0.5,
#            1., 2., 4., 8., 16., 32., 64., 128.]
# x = [math.log(f, 2) for f in factors]

# # os.chdir("/home/ian/thesis_data")
# # df = pd.read_csv("experiment_scale_distr.csv")
# # df_test = pd.read_csv("experiment_scale_kstest.csv")
# # if not os.path.exists("/home/ian/thesis_results/experiment_scale/"):
# #     os.mkdir("/home/ian/thesis_results/experiment_scale/")
# # os.chdir("/home/ian/thesis_results/experiment_scale/")

# os.chdir("/data/s3202844/data")
# df = pd.read_csv("experiment_scale_distr.csv")
# df_test = pd.read_csv("experiment_scale_kstest.csv")
# if not os.path.exists("/scratch/hyin/thesis_scripts/experiment_scale/"):
#     os.mkdir("/scratch/hyin/thesis_scripts/experiment_scale/")
# os.chdir("/scratch/hyin/thesis_scripts/experiment_scale/")

# dataset_list = df.values.tolist()
# columns = df.columns.values.tolist()
# feature_list = columns[8:]

# PVALUE = [[0 for _ in range(len(factors))] for _ in range(5)]
# fig = plt.figure(figsize=(14, 16))
# color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
# linestyle = ["-", "--", ":", "-.", "-"]
# for i in range(len(feature_list)):
#     ax = fig.add_subplot(8, 7, i + 1)
#     ax.set_yticks([])
#     ax.set_xticks([])
#     ax.axhline(0.05, color="red", linestyle=":")
#     for problem_id in range(1, 6):
#         # 2 lists for 2 plots
#         pvalue = []
#         wd = []
#         for j in range(len(factors)):
#             f = factors[j]
#             # parse pvalue
#             test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
#                                   (df_test["scale_factor"] == float(f)) &
#                                   (df_test["is_scale"] == 1.0)][
#                 feature_list[i]].tolist()[0]
#             test = string_to_list(test_string)
#             pvalue += [test[1]]
#             wd += [test[2]]
#             PVALUE[problem_id-1][j] += 1 if test[1] < 0.05 else 0
#         t_ind = int(len(feature_list[i]) / 2)
#         ax.plot(x, pvalue, color=color[problem_id - 1],
#                 linestyle=linestyle[problem_id - 1], linewidth=2,
#                 label="problem {}".format(problem_id))
# ax = fig.add_subplot(8, 7, 56)
# ax.set_yticks([])
# ax.xaxis.set_label_coords(0.5, 0.1)
# ax.yaxis.set_label_coords(0.1, 0.5)
# ax.set_xlabel(r'$\log_2 scale\_factor$', fontsize=14)
# ax.set_ylabel(r'p'+'-value', fontsize=14)
# ax.plot(x[0], x[0])
# ax.plot(x[-1], x[-1])
# for problem_id in range(1, 6):
#     ax.plot([0], [0], color=color[problem_id - 1],
#             linestyle=linestyle[problem_id - 1], linewidth=2,
#             label="problem {}".format(problem_id))
# ax.legend(loc="upper right", borderaxespad=0, ncol=1, fontsize=12)
# plt.tight_layout()
# plt.savefig("pvalue.png")
# plt.savefig("pvalue.eps", dpi=600, format='eps')
# plt.cla()
# plt.close()


# WD = [[0 for _ in range(len(factors))] for _ in range(5)]
# fig = plt.figure(figsize=(14, 16))
# color = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
# linestyle = ["-", "--", ":", "-.", "-"]
# for i in range(len(feature_list)):
#     ax = fig.add_subplot(8, 7, i + 1)
#     ax.set_yticks([])
#     ax.set_xticks([])
#     for problem_id in range(1, 6):
#         # 2 lists for 2 plots
#         pvalue = []
#         wd = []
#         for j in range(len(factors)):
#             f = factors[j]
#             # parse pvalue
#             test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
#                                   (df_test["scale_factor"] == float(f)) &
#                                   (df_test["is_scale"] == 1.0)][
#                 feature_list[i]].tolist()[0]
#             test = string_to_list(test_string)
#             pvalue += [test[1]]
#             wd += [test[2]]
#         wd_min = min(wd)
#         wd_max = max(wd)
#         for j in range(len(wd)):
#             if wd[j] == wd_min:
#                 wd[j] = 0.0
#             else:
#                 wd[j] = (wd[j] - wd_min) / (wd_max - wd_min)
#             if not math.isnan(wd[j] / (len(feature_list)*5)):
#                 WD[problem_id-1][j] += wd[j] / len(feature_list)
#         t_ind = int(len(feature_list[i]) / 2)
#         ax.plot(x, wd, color=color[problem_id - 1],
#                 linestyle=linestyle[problem_id - 1], linewidth=2,
#                 label="problem {}".format(problem_id))
# ax = fig.add_subplot(8, 7, 56)
# ax.set_yticks([])
# ax.xaxis.set_label_coords(0.5, 0.1)
# ax.yaxis.set_label_coords(0.1, 0.5)
# ax.set_xlabel(r'$\log_2 scale\_factor$', fontsize=14)
# ax.set_ylabel('EMD', fontsize=14)
# ax.plot(x[0], x[0])
# ax.plot(x[-1], x[-1])
# for problem_id in range(1, 6):
#     ax.plot([0], [0], color=color[problem_id - 1],
#             linestyle=linestyle[problem_id - 1], linewidth=2,
#             label="problem {}".format(problem_id))
# ax.legend(loc="upper right", borderaxespad=0, ncol=1, fontsize=12)
# plt.tight_layout()
# plt.savefig("wd.png")
# plt.savefig("wd.eps", dpi=600, format='eps')
# plt.cla()
# plt.close()


# f = open("aggregation.txt", "w")
# f.writelines([str(PVALUE)+'\n', str(WD)])
# f.close()


# # for problem_id in range(1, 6):
# #     if not os.path.exists("{}/".format(problem_id)):
# #         os.mkdir("{}/".format(problem_id))
# #     for i in range(len(feature_list)):
# #         if not os.path.exists("{}/{}/".format(problem_id, feature_list[i])):
# #             os.mkdir("{}/{}/".format(problem_id, feature_list[i]))
# #         # 2 lists for 2 plots
# #         PQf = []
# #         pvalue = []
# #         wd = []
# #         for f in factors:
# #             # parse distribution
# #             p_string = df[(df["problem_id"] == float(problem_id)) &
# #                           (df["is_scale"] == 0.0)][feature_list[i]].tolist()[0]
# #             q_string = df[(df["problem_id"] == float(problem_id)) &
# #                           (df["scale_factor"] == float(f)) &
# #                           (df["is_scale"] == 1.0)][feature_list[i]].tolist()[0]
# #             p = string_to_list(p_string)
# #             q = string_to_list(q_string)
# #             for j in range(len(p)):
# #                 PQf += [[p[j], q[j], f]]
# #             # parse pvalue
# #             test_string = df_test[(df_test["problem_id"] == float(problem_id)) &
# #                                   (df_test["scale_factor"] == float(f)) &
# #                                   (df_test["is_scale"] == 1.0)][
# #                 feature_list[i]].tolist()[0]
# #             test = string_to_list(test_string)
# #             pvalue += [test[1]]
# #             wd += [test[2]]
# #         # pvalue plot
# #         plt.figure(figsize=(5, 5))
# #         plt.ylim(-0.1, 1.1)
# #         plt.plot(x, pvalue)
# #         plt.axhline(0.05, color="red", linestyle=":")
# #         plt.xlabel("$\log_2{scale\_factor}$")
# #         plt.ylabel("$p$-value")
# #         plt.title("K-S test result of {}".format(feature_list[i]))
# #         plt.tight_layout()
# #         plt.savefig("{}/{}/{}_pvalue.png".format(problem_id, feature_list[i],
# #                                                  feature_list[i]))
# #         plt.cla()
# #         plt.close()
# #         # wd plot
# #         plt.figure(figsize=(5, 5))
# #         plt.plot(x, wd)
# #         plt.xlabel("$\log_2{scale\_factor}$")
# #         plt.ylabel("EMD")
# #         plt.title("EMD of {}".format(feature_list[i]))
# #         plt.tight_layout()
# #         plt.savefig("{}/{}/{}_wd.png".format(problem_id, feature_list[i],
# #                                              feature_list[i]))
# #         plt.cla()
# #         plt.close()
# #         # distribution plot
# #         PQf_df = pd.DataFrame(PQf, columns=["p", "q", "factor"])
# #         try:
# #             joypy.joyplot(PQf_df, by="factor", figsize=(6, 10),
# #                           color=["#1f77b4a0", "#ff7f0ea0"])
# #             rect1 = plt.Rectangle((0, 0), 0, 0, color='#1f77b4d0',
# #                                   label="basic distribution")
# #             rect2 = plt.Rectangle((0, 0), 0, 0, color='#ff7f0ed0',
# #                                   label="new distribution")
# #             plt.gca().add_patch(rect1)
# #             plt.gca().add_patch(rect2)
# #             plt.title("Distribution of {} over scale factors.".format(
# #                 feature_list[i]), fontsize=14)
# #             plt.xlabel("feature value", fontsize=14)
# #             plt.tight_layout()
# #             plt.legend(loc=3, fontsize=14)
# #             plt.savefig("{}/{}/{}_distr.png".format(problem_id,
# #                                                     feature_list[i],
# #                                                     feature_list[i]))
# #             plt.cla()
# #             plt.close()
# #         except ValueError:
# #             plt.cla()
# #             plt.close()
# #             print("{} only have None value!".format(feature_list[i]))
