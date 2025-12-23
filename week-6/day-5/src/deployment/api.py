from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import json
import uuid
from datetime import datetime
from pathlib import Path
import numpy as np


app = FastAPI(title="Titanic Survival Prediction API")

MODEL_PATH = Path("src/models/best_model.pkl")
FEATURE_PATH = Path("src/features/feature_list.json")
LOG_PATH = Path("prediction_logs.csv")

model = joblib.load(MODEL_PATH)

with open(FEATURE_PATH) as f:
    FEATURES = json.load(f)

class TitanicRequest(BaseModel):
    Pclass: int
    Sex: int
    Age: float
    SibSp: int
    Fare: float

def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[0, 12, 20, 40, 60],
        labels=[0, 1, 2, 3],
        include_lowest=True
    )

    df["Fare_log"] = np.log1p(df["Fare"])
    df["Fare_sqrt"] = np.sqrt(df["Fare"])

    df["IsChild"] = (df["Age"] < 16).astype(int)
    df["IsSenior"] = (df["Age"] > 50).astype(int)
    df["HighFare"] = (df["Fare"] > df["Fare"].median()).astype(int)

    df["FamilySize"] = df["SibSp"] + 1
    df["IsAlone"] = (df["FamilySize"] == 1).astype(int)

    df["Pclass_sq"] = df["Pclass"] ** 2
    df["Age_Fare"] = df["Age"] * df["Fare"]

    return df

@app.post("/predict")
def predict(request: TitanicRequest):
    request_id = str(uuid.uuid4())

    df = pd.DataFrame([request.dict()])
    df = engineer_features(df)

    df = df[FEATURES]

    prediction = int(model.predict(df)[0])
    probability = float(model.predict_proba(df)[0][1])

    log_row = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_id": request_id,
        "prediction": prediction,
        "probability": probability,
        **request.dict()
    }

    pd.DataFrame([log_row]).to_csv(
        LOG_PATH,
        mode="a",
        header=not LOG_PATH.exists(),
        index=False
    )

    return {
        "request_id": request_id,
        "survived": prediction,
        "survival_probability": round(probability, 4)
    }
