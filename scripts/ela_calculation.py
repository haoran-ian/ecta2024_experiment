import os
import re
import time
import warnings
import argparse
import numpy as np
import pandas as pd

from pflacco.classical_ela_features import calculate_dispersion
from pflacco.classical_ela_features import calculate_ela_distribution
from pflacco.classical_ela_features import calculate_ela_level
from pflacco.classical_ela_features import calculate_ela_meta
from pflacco.classical_ela_features import calculate_information_content
from pflacco.classical_ela_features import calculate_nbc
from pflacco.classical_ela_features import calculate_pca

warnings.filterwarnings("ignore")


def read_x(num_sampling, num_x):
    X = []
    m = num_x+1
    # f = open("/data/s3202844/data/samplingX.txt", "r")
    # f = open("/data/s3202844/data/samplingX_002D.txt", "r")
    f = open("config/samplingX_010D.txt", "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        x = []
        content = lines[m*i:m*i+m]
        for j in range(1, m):
            temp = []
            line = re.split(r"[ ]+", content[j][:-1])
            for n in line[1:]:
                temp += [float(n)]
            x += [temp]
        X += [x]
    return X


def read_y(path, num_sampling, num_x):
    Y = []
    f = open(path, "r")
    lines = f.readlines()
    f.close()
    for i in range(num_sampling):
        y = []
        line = lines[i][:-1].split(" ")
        for j in range(num_x):
            y += [float(line[j])]
        Y += [y]
    return Y


def ela_calculation(X, y):
    keys = []
    values = []

    disp = calculate_dispersion(X, y)
    keys += list(disp.keys())[:-1]
    values += list(disp.values())[:-1]
    ela_distr = calculate_ela_distribution(X, y)
    keys += list(ela_distr.keys())[:-1]
    values += list(ela_distr.values())[:-1]
    ela_level = calculate_ela_level(X, y)
    keys += list(ela_level.keys())[:-1]
    values += list(ela_level.values())[:-1]
    ela_meta = calculate_ela_meta(X, y)
    keys += list(ela_meta.keys())[:-1]
    values += list(ela_meta.values())[:-1]
    ic = calculate_information_content(X, y)
    keys += list(ic.keys())[:-1]
    values += list(ic.values())[:-1]
    nbc = calculate_nbc(X, y)
    keys += list(nbc.keys())[:-1]
    values += list(nbc.values())[:-1]
    pca = calculate_pca(X, y)
    keys += list(pca.keys())[:-1]
    values += list(pca.values())[:-1]

    return keys, values


if __name__ == "__main__":
    # meta data
    num_sampling = 100
    num_x = 1000
    dim = 10
    # # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", type=int, help="ID of the problem")
    parser.add_argument("-e", type=int, help="Which experiment? \
                        / 1: x translation / 2: x scaling / 3: x rotation \
                        / 4: y translation / 5: y scaling)")
    args = parser.parse_args()
    if args.i == None or args.e == None:
        parser.print_help()
        exit()
    problem_id = args.i
    case_id = args.e

    # read experiments results
    X = np.array(read_x(num_sampling, num_x))

    if case_id == 1:
        # x translation
        if not os.path.exists("ecta2024_data/x_translation/ela/"):
            os.makedirs("ecta2024_data/x_translation/ela/")
        prefix_name = ["problem_id", "d_x"]
        for i in range(1, 101):
            start_time = time.time()
            records = []
            prefix = [problem_id, i]
            file_path = f"ecta2024_data/x_translation/{problem_id}_{i:.6f}.txt"
            print(file_path)
            y = read_y(file_path, num_sampling, num_x)
            for j in range(num_sampling):
                keys, values = ela_calculation(X[j], y[j])
                records += [prefix + values]
            column_name = prefix_name + keys
            end_time = time.time()
            dataset_df = pd.DataFrame(records, columns=column_name)
            dataset_df.to_csv(
                f"ecta2024_data/x_translation/ela/{problem_id}_{i}.csv",
                index=False)
            print(f"x translation calculation time: {end_time - start_time}")
    elif case_id == 2:
        # x scaling
        if not os.path.exists("ecta2024_data/x_scaling/ela/"):
            os.makedirs("ecta2024_data/x_scaling/ela/")
        prefix_name = ["problem_id", "log_2^k"]
        k = -3.0
        while k < 3.1:
            if f"{k:.1f}" == "0.0":
                k += 0.1
                continue
            start_time = time.time()
            records = []
            prefix = [problem_id, k]
            file_path = f"ecta2024_data/x_scaling/{problem_id}_{k:.6f}.txt"
            print(file_path)
            y = read_y(file_path, num_sampling, num_x)
            for j in range(num_sampling):
                keys, values = ela_calculation(X[j], y[j])
                records += [prefix + values]
            column_name = prefix_name + keys
            end_time = time.time()
            dataset_df = pd.DataFrame(records, columns=column_name)
            dataset_df.to_csv(
                f"ecta2024_data/x_scaling/ela/{problem_id}_{k:.1f}.csv",
                index=False)
            print(f"x scaling calculation time: {end_time - start_time}")
            k += 0.1
    elif case_id == 3:
        # x rotation
        if not os.path.exists("ecta2024_data/x_rotation/ela/"):
            os.makedirs("ecta2024_data/x_rotation/ela/")
        prefix_name = ["problem_id", "matrix_id"]
        for i in range(100):
            start_time = time.time()
            records = []
            prefix = [problem_id, i]
            file_path = f"ecta2024_data/x_rotation/{problem_id}_{i}.txt"
            print(file_path)
            y = read_y(file_path, num_sampling, num_x)
            for j in range(num_sampling):
                keys, values = ela_calculation(X[j], y[j])
                records += [prefix + values]
            column_name = prefix_name + keys
            end_time = time.time()
            dataset_df = pd.DataFrame(records, columns=column_name)
            dataset_df.to_csv(
                f"ecta2024_data/x_rotation/ela/{problem_id}_{i}.csv",
                index=False)
            print(f"x rotation calculation time: {end_time - start_time}")
    elif case_id == 4:
        # y translation
        if not os.path.exists("ecta2024_data/y_translation/ela/"):
            os.makedirs("ecta2024_data/y_translation/ela/")
        prefix_name = ["problem_id", "dy"]
        for dy in range(50, 1001, 50):
            start_time = time.time()
            records = []
            prefix = [problem_id, dy]
            file_path = f"ecta2024_data/y_translation/{problem_id}_{dy}.txt"
            print(file_path)
            y = read_y(file_path, num_sampling, num_x)
            for j in range(num_sampling):
                keys, values = ela_calculation(X[j], y[j])
                records += [prefix + values]
            column_name = prefix_name + keys
            end_time = time.time()
            dataset_df = pd.DataFrame(records, columns=column_name)
            dataset_df.to_csv(
                f"ecta2024_data/y_translation/ela/{problem_id}_{dy}.csv",
                index=False)
            print(f"y translation calculation time: {end_time - start_time}")
    elif case_id == 5:
        # y scaling
        if not os.path.exists("ecta2024_data/y_scaling/ela/"):
            os.makedirs("ecta2024_data/y_scaling/ela/")
        prefix_name = ["problem_id", "log_2^k"]
        k = -3.0
        while k < 3.1:
            if f"{k:.1f}" == "0.0":
                k += 0.1
                continue
            start_time = time.time()
            records = []
            prefix = [problem_id, k]
            file_path = f"ecta2024_data/y_scaling/{problem_id}_{k:.6f}.txt"
            print(file_path)
            y = read_y(file_path, num_sampling, num_x)
            for j in range(num_sampling):
                keys, values = ela_calculation(X[j], y[j])
                records += [prefix + values]
            column_name = prefix_name + keys
            end_time = time.time()
            dataset_df = pd.DataFrame(records, columns=column_name)
            dataset_df.to_csv(
                f"ecta2024_data/y_scaling/ela/{problem_id}_{k:.1f}.csv",
                index=False)
            print(f"y scaling calculation time: {end_time - start_time}")
            k += 0.1
