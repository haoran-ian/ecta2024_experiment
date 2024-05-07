import os
import sqlite3
import pandas as pd


def redirect_rotation(df, conn):
    sql_query = f"SELECT * FROM trace"
    df_trace = pd.read_sql_query(sql_query, conn)
    id_to_trace_dict = df_trace.set_index("matrix_id")["trace"].to_dict()
    df["trace"] = df["matrix_id"].map(id_to_trace_dict)
    position = df.columns.get_loc("matrix_id")
    df.insert(position, "trace_new", df["trace"])
    df.drop(["matrix_id", "trace"], axis=1, inplace=True)
    df.rename(columns={"trace_new": "trace"}, inplace=True)
    return df


def parse_transformations(transformation, conn):
    print(f"Processing {transformation} to database...")
    df = pd.DataFrame()
    if transformation == "x_translation":
        for i in range(1, 6):
            for j in range(1, 41):
                file_name = f"ecta2024_data/x_translation/ela/{i}_{j}.csv"
                df_prob = pd.read_csv(file_name)
                df = df_prob if df.empty else pd.concat([df, df_prob], axis=0)
    else:
        file_names = os.listdir(f"ecta2024_data/{transformation}/ela")
        for file_name in file_names:
            df_prob = pd.read_csv(
                f"ecta2024_data/{transformation}/ela/{file_name}")
            if transformation == "origin":
                df_prob = df_prob.drop("log_2^k", axis=1)
            df = df_prob if df.empty else pd.concat([df, df_prob], axis=0)
    if transformation == "x_rotation":
        df = redirect_rotation(df, conn)
    elif transformation == "y_translation":
        df = df.rename(columns={"dy": "d_y"})
    df.to_sql(f"{transformation}", conn, index=False)


if __name__ == "__main__":
    transformations = ["origin", "x_rotation", "x_scaling",
                       "x_translation", "y_scaling", "y_translation"]
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    for transformation in transformations:
        cursor = conn.cursor()
        cursor.execute(f"select name from sqlite_master where type='table' and \
            name='{transformation}'")
        if cursor.fetchone():
            cursor.execute(f"drop table {transformation}")
        parse_transformations(transformation, conn)
    conn.close()
    print("Done!")
