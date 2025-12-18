import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import json
from pathlib import Path

# paths
INPUT_DATA = Path("/home/vidhiajmera/launchpad/week-6/day-2/src/data/processed/final.csv")
OUTPUT_DIR = Path("/home/vidhiajmera/launchpad/week-6/day-2/src/data/processed/")

def load_data():
    return pd.read_csv(INPUT_DATA)

def create_features(df):
    # Drop identifier & text columns
    drop_cols = [
        "PassengerId", "Name", "Ticket", "Cabin", "Embarked"
    ]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    # Encode Sex
    if "Sex" in df.columns:
        df["Sex"] = df["Sex"].map({"male": 0, "female": 1})

    # Target
    y = df["Survived"]
    X = df.drop(columns=["Survived"])

    # -------- Feature Engineering --------
    X["AgeGroup"] = pd.cut(X["Age"], bins=[0, 12, 20, 40, 60], labels=[0, 1, 2, 3])
    X["Fare_log"] = np.log1p(X["Fare"])
    X["Fare_sqrt"] = np.sqrt(X["Fare"])
    X["IsChild"] = (X["Age"] < 16).astype(int)
    X["IsSenior"] = (X["Age"] > 50).astype(int)
    X["HighFare"] = (X["Fare"] > X["Fare"].median()).astype(int)
    X["FamilySize"] = X["SibSp"] + 1
    X["IsAlone"] = (X["FamilySize"] == 1).astype(int)
    X["Pclass_sq"] = X["Pclass"] ** 2
    X["Age_Fare"] = X["Age"] * X["Fare"]

    # Drop zero-variance column
    if "Parch" in X.columns:
        X = X.drop(columns=["Parch"])

    return X, y

def scale_features(X):
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(
        scaler.fit_transform(X),
        columns=X.columns
    )
    return X_scaled

def split_data(X, y):
    return train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

def save_outputs(X_train, X_test, y_train, y_test):
    OUTPUT_DIR.mkdir(exist_ok=True)

    X_train.to_csv(OUTPUT_DIR / "X_train.csv", index=False)
    X_test.to_csv(OUTPUT_DIR / "X_test.csv", index=False)
    y_train.to_csv(OUTPUT_DIR / "y_train.csv", index=False)
    y_test.to_csv(OUTPUT_DIR / "y_test.csv", index=False)

def save_feature_list(features):
    with open("/home/vidhiajmera/launchpad/week-6/day-2/src/features/feature_list.json", "w") as f:
        json.dump(features, f, indent=4)

def main():
    df = load_data()
    X, y = create_features(df)
    X = scale_features(X)
    X_train, X_test, y_train, y_test = split_data(X, y)
    save_outputs(X_train, X_test, y_train, y_test)
    save_feature_list(list(X.columns))

    print("Feature engineering completed")
    print("Train/Test data saved")

if __name__ == "__main__":
    main()
