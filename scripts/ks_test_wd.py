import sys
import sqlite3
import pandas as pd

from scipy.stats import ks_2samp, wasserstein_distance


def parse_unique_header(experiment_table):
    unique_header = []
    experiment_list = experiment_table.values.tolist()
    for rec in experiment_list:
        if rec[:8] not in unique_header:
            unique_header += [rec[:8]]
    return unique_header


def parse_distribution(experiment_table, unique_header):
    columns = experiment_table.columns.values.tolist()
    num_header = len(unique_header)
    num_feature = len(columns)-8
    experiment_list = experiment_table.values.tolist()
    distr = [[[] for _ in range(num_feature+8)] for _ in range(num_header)]
    for i in range(num_header):
        for j in range(8):
            distr[i][j] = unique_header[i][j]
        for rec in experiment_list:
            if rec[:8] == unique_header[i]:
                for j in range(num_feature):
                    distr[i][j+8] += [rec[j+8]]
    return distr


def kstest(distr):
    def head_equal(a, b):
        result = True
        for i in range(8):
            if i == 1:
                continue
            if a[i] != b[i]:
                result = False
        return result
    basic_distr = []
    for rec in distr:
        if int(rec[5]) == 0 and int(rec[6]) == 0 and int(rec[7]) == 0:
            basic_distr += [rec]
    distr_headers = []
    for rec in distr:
        if int(rec[5]) == 1 or int(rec[6]) == 1 or int(rec[7]) == 1:
            if int(rec[1]) == 0:
                distr_headers += [rec[:8]]
    dataset_distr = [[[] for _ in range(len(distr[0])-8)]
                     for _ in range(len(distr_headers))]
    for i in range(len(distr_headers)):
        h = distr_headers[i]
        for rec in distr:
            if head_equal(h, rec[:8]):
                for j in range(len(dataset_distr[0])):
                    dataset_distr[i][j] += rec[j+8]
    dataset_kstest = [[None for _ in range(
        len(distr[0]))] for _ in range(len(dataset_distr))]
    for i in range(len(dataset_distr)):
        for rec in basic_distr:
            if rec[0] == distr_headers[i][0]:
                basic_distr_ = rec
        for j in range(8):
            dataset_kstest[i][j] = distr_headers[i][j]
        for j in range(len(dataset_distr[0])):
            p = basic_distr_[j+8]
            q = dataset_distr[i][j]
            statistic, pvalue = ks_2samp(p, q)
            wd = wasserstein_distance(p, q)
            dataset_kstest[i][j+8] = [statistic, pvalue, wd]
    return dataset_kstest


if __name__ == "__main__":
    transformations = ["origin", "x_scaling", "y_scaling", "y_translation"]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    for transformation in transformations:
        cursor = conn.cursor()
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}")
