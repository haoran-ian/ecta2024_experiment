import os
import sqlite3
import numpy as np
import pandas as pd


def generate_tvec(low, high):
    arr = np.zeros(10)
    special_index = np.random.randint(0, 10)
    arr[special_index] = np.random.uniform(
        low, high) * np.random.choice([-1, 1])
    for i in range(10):
        if i != special_index:
            arr[i] = np.random.uniform(-high, high)
    return arr


if __name__ == "__main__":
    if not os.path.exists("config/tvec.txt"):
        print("Generating tvecs, file saved at config/tvec.txt")
        tvecs = []
        for i in range(50):
            for j in range(20):
                low = j * 5
                high = low + 5
                tvec = generate_tvec(low, high)
                tvecs += [tvec.tolist()]
        np.savetxt("config/tvec.txt", np.array(tvecs))
    conn = sqlite3.connect("ecta2024_data/atom_data.db")
    cursor = conn.cursor()
    cursor.execute(f"select name from sqlite_master where type='table' and \
        name='tvec'")
    if cursor.fetchone():
        cursor.execute(f"drop table tvec")
    values = []
    tvecs = np.loadtxt("config/tvec.txt")
    tvec_l1 = np.max(np.abs(tvecs), axis=1)
    for i in range(tvec_l1.shape[0]):
        values += [[i, int(tvec_l1[i]/5)*5+5]]
    df = pd.DataFrame(data=values, columns=["tvec_id", "translation distance"])
    df.to_sql("tvec", conn, index=False)
