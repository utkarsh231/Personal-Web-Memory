import sqlite3
import os
from shutil import copyfile
import pandas as pd

def extract_history(limit=100):
    history_path = os.path.expanduser("~/Library/Application Support/Google/Chrome/Default/History")
    temp_path = "./data/History_temp"

    os.makedirs("data", exist_ok=True)
    copyfile(history_path, temp_path)

    conn = sqlite3.connect(temp_path)
    df = pd.read_sql_query(
        f"""
        SELECT url, title, last_visit_time
        FROM urls
        ORDER BY last_visit_time DESC
        LIMIT {limit};
        """,
        conn,
    )
    conn.close()

    df.to_csv("./data/chrome_history.csv", index=False)
    print("Saved chrome history csv")

if __name__ == "__main__":
    extract_history()

