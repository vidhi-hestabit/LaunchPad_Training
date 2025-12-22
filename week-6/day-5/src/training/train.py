import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix
)

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from xgboost import XGBClassifier

# ---------------- PATHS ----------------
DATA_DIR = Path("src/data/processed")
MODEL_DIR = Path("src/models")
EVAL_DIR = Path("src/evaluation")

MODEL_DIR.mkdir(parents=True, exist_ok=True)
EVAL_DIR.mkdir(parents=True, exist_ok=True)

# ---------------- LOAD DATA ----------------
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").values.ravel()
X_test  = pd.read_csv(DATA_DIR / "X_test.csv")
y_test  = pd.read_csv(DATA_DIR / "y_test.csv").values.ravel()

# ---------------- MODELS ----------------
models = {
    "LogisticRegression": LogisticRegression(
        penalty="l2", C=1.0, max_iter=1000
    ),
    "RandomForest": RandomForestClassifier(
        n_estimators=200, max_depth=6, random_state=42
    ),
    "XGBoost": XGBClassifier(
        n_estimators=200, learning_rate=0.05,
        max_depth=4, subsample=0.8,
        eval_metric="logloss", random_state=42
    ),
    "NeuralNetwork": MLPClassifier(
        hidden_layer_sizes=(64, 32),
        alpha=0.001, max_iter=500, random_state=42
    )
}

# ---------------- CV SETUP ----------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

results = {}

# ---------------- TRAINING LOOP ----------------
for name, model in models.items():
    print(f"\nTraining {name}...")
    
    metrics = {
        "accuracy": [], "precision": [],
        "recall": [], "f1": [], "roc_auc": []
    }

    for train_idx, val_idx in cv.split(X_train, y_train):
        X_tr, X_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
        y_tr, y_val = y_train[train_idx], y_train[val_idx]

        model.fit(X_tr, y_tr)
        y_pred = model.predict(X_val)
        y_prob = model.predict_proba(X_val)[:, 1]

        metrics["accuracy"].append(accuracy_score(y_val, y_pred))
        metrics["precision"].append(precision_score(y_val, y_pred))
        metrics["recall"].append(recall_score(y_val, y_pred))
        metrics["f1"].append(f1_score(y_val, y_pred))
        metrics["roc_auc"].append(roc_auc_score(y_val, y_prob))

    results[name] = {k: np.mean(v) for k, v in metrics.items()}

# ---------------- BEST MODEL ----------------
best_model_name = max(results, key=lambda x: results[x]["roc_auc"])
best_model = models[best_model_name]

print(f"\nBest Model: {best_model_name}")

best_model.fit(X_train, y_train)
joblib.dump(best_model, MODEL_DIR / "best_model.pkl")

# ---------------- TEST EVALUATION ----------------
y_test_pred = best_model.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)

plt.figure(figsize=(5, 4))
plt.imshow(cm)
plt.title("Confusion Matrix")
plt.colorbar()
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.tight_layout()
plt.savefig(EVAL_DIR / "confusion_matrix.png")
plt.close()

# ---------------- SAVE METRICS ----------------
with open(EVAL_DIR / "metrics.json", "w") as f:
    json.dump(results, f, indent=4)

print("Training complete. Metrics & model saved.")
