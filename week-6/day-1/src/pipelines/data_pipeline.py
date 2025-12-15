import pandas as pd
import numpy as np
from pathlib import Path

# paths
RAW_DATA_PATH = Path("/home/vidhiajmera/launchpad/week-6/day-1/src/data/raw/dataset.csv")
PROCESSED_DATA_PATH = Path("/home/vidhiajmera/launchpad/week-6/day-1/src/data/processed/final.csv")

def load_data():
    print("Loading data...")
    return pd.read_csv(RAW_DATA_PATH)

def clean_data(df):
    print("Cleaning data...")

    # drop duplicate rows
    df = df.drop_duplicates()

    # handle missing values
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna(df[col].mode()[0])

    return df

def remove_outliers(df):
    print("Removing outliers using IQR...")
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]

    return df

def save_data(df):
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print("Cleaned dataset saved to data/processed/final.csv")

def main():
    df = load_data()
    df = clean_data(df)
    df = remove_outliers(df)
    save_data(df)

if __name__ == "__main__":
    main()
