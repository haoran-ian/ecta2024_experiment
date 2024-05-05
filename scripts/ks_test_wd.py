import sys
import sqlite3
import numpy as np
import pandas as pd

from scipy.stats import ks_2samp, wasserstein_distance


def x_scaling_analysis(conn):
    sql_query = "SELECT * FROM origin"
    df_origin = pd.read_sql_query(sql_query, conn)
    df_origin.insert(1, "log_2^k", 0.)
    sql_query = "SELECT * FROM x_scaling"
    df_x_scaling = pd.read_sql_query(sql_query, conn)
    grouped_p = df_origin.groupby(
        ["problem_id", "log_2^k"]).agg(list).reset_index()
    grouped_q = df_x_scaling.groupby(
        ["problem_id", "log_2^k"]).agg(list).reset_index().values
    analysis = [[] for _ in range(3)]
    for i in range(grouped_q.shape[0]):
        for j in range(3):
            analysis[j] += [grouped_q[i][:2].tolist()]
        for j in range(2, grouped_q.shape[1]):
            problem_id = grouped_q[i][0]
            p = np.array(grouped_p[(grouped_p["problem_id"] == problem_id)
                                   ][grouped_p.columns[j]].values[0])
            q = np.array(grouped_q[i][j])
            pq_max = max(np.max(p), np.max(q))
            pq_min = min(np.min(p), np.min(q))
            if pq_max - pq_min == 0:
                p[:] = 0
                q[:] = 0
            else:
                p = (np.array(p) - pq_min) / (pq_max - pq_min)
                q = (np.array(q) - pq_min) / (pq_max - pq_min)
            statistic, pvalue = ks_2samp(p, q)
            emd = wasserstein_distance(p, q)
            analysis[0][-1] += [statistic]
            analysis[1][-1] += [pvalue]
            analysis[2][-1] += [emd]
    analysis = np.array(analysis)
    df = pd.DataFrame(analysis[0], columns=df_x_scaling.columns)
    df.to_sql("x_scaling_ks_statistic", conn, index=False)
    df = pd.DataFrame(analysis[1], columns=df_x_scaling.columns)
    df.to_sql("x_scaling_ks_pvalue", conn, index=False)
    df = pd.DataFrame(analysis[2], columns=df_x_scaling.columns)
    df.to_sql("x_scaling_emd", conn, index=False)


def y_scaling_analysis(conn):
    sql_query = "SELECT * FROM origin"
    df_origin = pd.read_sql_query(sql_query, conn)
    df_origin.insert(1, "log_2^k", 0.)
    sql_query = "SELECT * FROM y_scaling"
    df_y_scaling = pd.read_sql_query(sql_query, conn)
    grouped_p = df_origin.groupby(
        ["problem_id", "log_2^k"]).agg(list).reset_index()
    grouped_q = df_y_scaling.groupby(
        ["problem_id", "log_2^k"]).agg(list).reset_index().values
    analysis = [[] for _ in range(3)]
    for i in range(grouped_q.shape[0]):
        for j in range(3):
            analysis[j] += [grouped_q[i][:2].tolist()]
        for j in range(2, grouped_q.shape[1]):
            problem_id = grouped_q[i][0]
            p = np.array(grouped_p[(grouped_p["problem_id"] == problem_id)
                                   ][grouped_p.columns[j]].values[0])
            q = np.array(grouped_q[i][j])
            pq_max = max(np.max(p), np.max(q))
            pq_min = min(np.min(p), np.min(q))
            if pq_max - pq_min == 0:
                p[:] = 0
                q[:] = 0
            else:
                p = (np.array(p) - pq_min) / (pq_max - pq_min)
                q = (np.array(q) - pq_min) / (pq_max - pq_min)
            statistic, pvalue = ks_2samp(p, q)
            emd = wasserstein_distance(p, q)
            analysis[0][-1] += [statistic]
            analysis[1][-1] += [pvalue]
            analysis[2][-1] += [emd]
    analysis = np.array(analysis)
    df = pd.DataFrame(analysis[0], columns=df_y_scaling.columns)
    df.to_sql("y_scaling_ks_statistic", conn, index=False)
    df = pd.DataFrame(analysis[1], columns=df_y_scaling.columns)
    df.to_sql("y_scaling_ks_pvalue", conn, index=False)
    df = pd.DataFrame(analysis[2], columns=df_y_scaling.columns)
    df.to_sql("y_scaling_emd", conn, index=False)


def y_translation_analysis(conn):
    sql_query = "SELECT * FROM origin"
    df_origin = pd.read_sql_query(sql_query, conn)
    df_origin.insert(1, "dy", 0.)
    sql_query = "SELECT * FROM y_translation"
    df_y_translation = pd.read_sql_query(sql_query, conn)
    grouped_p = df_origin.groupby(
        ["problem_id", "dy"]).agg(list).reset_index()
    grouped_q = df_y_translation.groupby(
        ["problem_id", "dy"]).agg(list).reset_index().values
    analysis = [[] for _ in range(3)]
    for i in range(grouped_q.shape[0]):
        for j in range(3):
            analysis[j] += [grouped_q[i][:2].tolist()]
        for j in range(2, grouped_q.shape[1]):
            problem_id = grouped_q[i][0]
            p = np.array(grouped_p[(grouped_p["problem_id"] == problem_id)
                                   ][grouped_p.columns[j]].values[0])
            q = np.array(grouped_q[i][j])
            pq_max = max(np.max(p), np.max(q))
            pq_min = min(np.min(p), np.min(q))
            if pq_max - pq_min == 0:
                p[:] = 0
                q[:] = 0
            else:
                p = (np.array(p) - pq_min) / (pq_max - pq_min)
                q = (np.array(q) - pq_min) / (pq_max - pq_min)
            statistic, pvalue = ks_2samp(p, q)
            emd = wasserstein_distance(p, q)
            analysis[0][-1] += [statistic]
            analysis[1][-1] += [pvalue]
            analysis[2][-1] += [emd]
    analysis = np.array(analysis)
    df = pd.DataFrame(analysis[0], columns=df_y_translation.columns)
    df.to_sql("y_translation_ks_statistic", conn, index=False)
    df = pd.DataFrame(analysis[1], columns=df_y_translation.columns)
    df.to_sql("y_translation_ks_pvalue", conn, index=False)
    df = pd.DataFrame(analysis[2], columns=df_y_translation.columns)
    df.to_sql("y_translation_emd", conn, index=False)


if __name__ == "__main__":
    transformations = ["x_scaling", "y_scaling", "y_translation"]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    for transformation in transformations:
        cursor = conn.cursor()
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}_ks_statistic'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}_ks_statistic")
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}_ks_pvalue'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}_ks_pvalue")
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}_emd'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}_emd")

        if transformation == "x_scaling":
            x_scaling_analysis(conn)
        elif transformation == "y_scaling":
            y_scaling_analysis(conn)
        elif transformation == "y_translation":
            y_translation_analysis(conn)
