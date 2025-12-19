from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import uuid
from datetime import datetime
import os
app = FastAPI(title="Package Predictor ML")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js
    allow_credentials=True,
    allow_methods=["*"],   # Allows OPTIONS, POST, GET, etc
    allow_headers=["*"],
)
# ---------- Model Loading (FIXED) ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models", "model.joblib")

model = joblib.load(MODEL_PATH)

class PredictionRequest(BaseModel):
    age: int = Field(..., ge=18)
    experience_years: int = Field(..., ge=0)
    tech_count: int = Field(..., ge=1)
    primary_tech: str
    education_level: str

class PredictionResponse(BaseModel):
    request_id: str
    predicted_package_lpa: float
    timestamp: str

@app.post("/predict", response_model=PredictionResponse)
def predict(req: PredictionRequest):
    df = pd.DataFrame([req.dict()])
    prediction = model.predict(df)[0]

    return PredictionResponse(
        request_id=str(uuid.uuid4()),
        predicted_package_lpa=round(float(prediction), 2),
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/health")
def health():
    return {"status": "ok"}
