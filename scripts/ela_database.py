import os
import re
import sqlite3
import numpy as np
import pandas as pd


def parse_origin(file_names, conn):
    df = pd.DataFrame()
    for file_name in file_names:
        problem_id = int(file_name.split("_")[0])
        df_prob = pd.read_csv(f"ecta2024_data/origin/ela/{file_name}")
        df_prob = df_prob.drop("log_2^k", axis=1)
        if df.empty:
            df = df_prob
        else:
            df = pd.concat([df, df_prob], axis=0)
    df.to_sql("origin", conn, index=False)


def parse_x_scaling(file_names, conn):
    df = pd.DataFrame()
    for file_name in file_names:
        # pattern = r"-?\d+\.\d+|-?\d+"
        # numbers = re.findall(pattern, file_name)
        # problem_id = int(numbers[0])
        # k = float(numbers[1])
        df_prob = pd.read_csv(f"ecta2024_data/x_scaling/ela/{file_name}")
        if df.empty:
            df = df_prob
        else:
            df = pd.concat([df, df_prob], axis=0)
    df.to_sql("x_scaling", conn, index=False)


def parse_x_translation(file_names, conn):
    pass


def parse_y_scaling(file_names, conn):
    df = pd.DataFrame()
    for file_name in file_names:
        # pattern = r"-?\d+\.\d+|-?\d+"
        # numbers = re.findall(pattern, file_name)
        # problem_id = int(numbers[0])
        # k = float(numbers[1])
        df_prob = pd.read_csv(f"ecta2024_data/y_scaling/ela/{file_name}")
        if df.empty:
            df = df_prob
        else:
            df = pd.concat([df, df_prob], axis=0)
    df.to_sql("y_scaling", conn, index=False)


def parse_y_translation(file_names, conn):
    df = pd.DataFrame()
    for file_name in file_names:
        df_prob = pd.read_csv(f"ecta2024_data/y_translation/ela/{file_name}")
        if df.empty:
            df = df_prob
        else:
            df = pd.concat([df, df_prob], axis=0)
    df = df.rename(columns={'dy': 'd_y'})
    df.to_sql("y_translation", conn, index=False)


if __name__ == "__main__":
    transformations = ["origin", "x_scaling", "y_scaling", "y_translation"]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    for transformation in transformations:
        cursor = conn.cursor()
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}")
        file_names = os.listdir(f"ecta2024_data/{transformation}/ela")
        if transformation == "origin":
            parse_origin(file_names, conn)
        elif transformation == "x_scaling":
            parse_x_scaling(file_names, conn)
        elif transformation == "y_scaling":
            parse_y_scaling(file_names, conn)
        elif transformation == "y_translation":
            parse_y_translation(file_names, conn)
        # table_values = read_atom_array(table_name)
        # df = array_to_dataframe(table_values, table_name)
        # df.to_sql(table_name, conn, index=False)
        # print(table_name)
