import pandas as pd
import json
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score

DATA_DIR = Path("src/data/processed")
TUNING_DIR = Path("src/tuning")

TUNING_DIR.mkdir(parents=True, exist_ok=True)

X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").values.ravel()

rf = RandomForestClassifier(random_state=42)

param_grid = {
    "n_estimators": [100, 200, 300],
    "max_depth": [4, 6, 8],
    "min_samples_split": [2, 5],
    "min_samples_leaf": [1, 2]
}

grid = GridSearchCV(
    rf,
    param_grid=param_grid,
    cv=5,
    scoring="roc_auc",
    n_jobs=-1
)

print("Running GridSearch...")
grid.fit(X_train, y_train)

results = {
    "best_params": grid.best_params_,
    "best_score": grid.best_score_
}

with open(TUNING_DIR / "results.json", "w") as f:
    json.dump(results, f, indent=4)

print("Best Parameters:", grid.best_params_)
print("Best ROC-AUC:", grid.best_score_)
