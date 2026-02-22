import pandas as pd

def load_and_clean_data(path):
    df = pd.read_csv(path)

    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Course_Name", "Date"])

    return df